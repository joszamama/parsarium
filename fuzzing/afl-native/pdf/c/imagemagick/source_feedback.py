"""Compare two valid PDFs in the ImageMagick PDF images and write source-feedback.json.

Run from the repository root after both images exist:

    python3 parsarium.py build pdf c imagemagick
    python3 parsarium.py afl build pdf c imagemagick
    python3 fuzzing/afl-native/pdf/c/imagemagick/source_feedback.py

The base image replays each control with LLVM source coverage and reports
line hit-count differences in the ImageMagick PDF coder and the Ghostscript
pdfi interpreter. The AFL++ image runs afl-showmap on the same two files.
Only valid controls are used; no campaign is started.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
BASE_IMAGE = "parsarium/pdf-c-imagemagick:local"
AFL_IMAGE = "parsarium-afl/pdf-c-imagemagick:local"
CASES = (("control", "controls/pdf/one-page.pdf", {"pages": 1, "width": 612, "height": 792}),
         ("valid_variant", "controls/pdf/two-page.pdf", {"pages": 2, "width": 612, "height": 792}))
GROUPS = {"pdf_coder": ("/work/source/", "/coders/pdf.c"),
          "ghostscript_bridge": ("/work/source/", "/coders/ghostscript-private.h"),
          "pdfi_interpreter": ("/work/ghostscript/pdf/", ""),
          "rendered_page_png_decode": ("/work/source/", "/coders/png.c")}

# Runs inside the base image: replay one case and print line hit counts per group.
LINES = r"""
import json, subprocess, sys
groups = json.loads(sys.argv[1])
lcov = subprocess.run(['llvm-cov', 'export', '/work/replay', '-object=/work/lib/libgs.so',
                       '-instr-profile=/coverage/case.profdata', '-format=lcov'],
                      check=True, capture_output=True, text=True).stdout
hits, name, keys = {key: {} for key in groups}, None, []
for line in lcov.splitlines():
    if line.startswith('SF:'):
        name = line[3:]
        keys = [k for k, (p, s) in groups.items() if name.startswith(p) and name.endswith(s)]
    elif line.startswith('DA:') and keys:
        number, count = line[3:].split(',')[:2]
        for key in keys:
            hits[key][f'{name}:{number}'] = int(count)
print(json.dumps(hits))
"""


def docker(args: list[str]) -> str:
    result = subprocess.run(["docker", *args], cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-4000:])
    return result.stdout


def sandbox(case: Path, coverage: Path) -> list[str]:
    return ["run", "--rm", "--platform", "linux/arm64", "--network", "none", "--read-only",
            "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}", "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
            "-v", f"{case}:/input/case:ro", "-v", f"{coverage}:/coverage"]


def source_lines(case: Path, coverage: Path) -> tuple[dict, dict]:
    script = ("LLVM_PROFILE_FILE=/coverage/case-%m.profraw /work/replay /input/case > /coverage/observed.json"
              " && llvm-profdata merge -sparse /coverage/case-*.profraw -o /coverage/case.profdata"
              ' && python3 -c "$0" "$1"')
    hits = json.loads(docker([*sandbox(case, coverage), "--entrypoint", "/bin/sh", BASE_IMAGE,
                              "-c", script, LINES, json.dumps(GROUPS)]))
    return json.loads((coverage / "observed.json").read_text()), hits


def afl_edges(case: Path, coverage: Path, map_size: int) -> set[str]:
    docker([*sandbox(case, coverage), "-e", f"AFL_MAP_SIZE={map_size}", "--entrypoint", "afl-showmap",
            AFL_IMAGE, "-q", "-m", "none", "-t", "10000", "-o", "/coverage/edges.txt",
            "--", "/work/fuzzer", "/input/case"])
    return {line.split(":", 1)[0] for line in (coverage / "edges.txt").read_text().splitlines() if line}


def main() -> None:
    probe = subprocess.run(["docker", "run", "--rm", "--platform", "linux/arm64",
                            "-e", "AFL_DUMP_MAP_SIZE=1", "--entrypoint", "/work/fuzzer",
                            AFL_IMAGE], cwd=ROOT, capture_output=True, text=True)
    if not probe.stdout.strip().isdigit():
        raise RuntimeError(f"AFL++ map size probe failed: {probe.stderr[-1000:]}")
    map_size = int(probe.stdout.strip())
    observed, hits, edges, records = {}, {}, {}, {}
    for key, relative, expected in CASES:
        case = ROOT / relative
        with tempfile.TemporaryDirectory(prefix="parsarium-im-pdf-") as temporary:
            observed[key], hits[key] = source_lines(case, Path(temporary))
        if observed[key] != expected:
            raise SystemExit(f"{relative}: expected {expected}, observed {observed[key]}")
        with tempfile.TemporaryDirectory(prefix="parsarium-im-pdf-afl-") as temporary:
            edges[key] = afl_edges(case, Path(temporary), map_size)
        records[key] = {"path": relative, "sha256": sha256(case.read_bytes()).hexdigest(),
                        "output": observed[key], "feedback_edges": len(edges[key])}
    differential = {}
    for group in GROUPS:
        first, second = hits["control"][group], hits["valid_variant"][group]
        differential[group] = {
            "control_lines_covered": sum(1 for count in first.values() if count),
            "variant_lines_covered": sum(1 for count in second.values() if count),
            "lines_with_changed_hit_count": sum(1 for line in first.keys() | second.keys()
                                                if first.get(line, 0) != second.get(line, 0)),
        }
    sensitive = all(differential[group]["lines_with_changed_hit_count"] > 0
                    for group in ("pdf_coder", "pdfi_interpreter"))
    variant_only = len(edges["valid_variant"] - edges["control"])
    report = {
        "schema_version": 1,
        "engine": "afl-showmap 4.33c and LLVM source line counts, one fixed valid PDF per run",
        "command": "afl-showmap -q -m none -t 10000 -o OUTPUT -- /work/fuzzer /input/case",
        "base_image_id": docker(["image", "inspect", BASE_IMAGE, "--format", "{{.Id}}"]).strip(),
        "afl_image_id": docker(["image", "inspect", AFL_IMAGE, "--format", "{{.Id}}"]).strip(),
        "afl_map_size": map_size,
        **records,
        "shared_edge_ids": len(edges["control"] & edges["valid_variant"]),
        "control_only_edge_ids": len(edges["control"] - edges["valid_variant"]),
        "variant_only_edge_ids": variant_only,
        "source_differential": differential,
        "rendered_page_png_decode_note": "PNG decode of Ghostscript output is image decoding, not PDF parsing",
        "pass": sensitive and variant_only > 0,
    }
    (HERE / "source-feedback.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if not report["pass"]:
        raise SystemExit("PDF parser differences did not reach source coverage and AFL++ edges")


if __name__ == "__main__":
    main()
