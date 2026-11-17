"""Compare AFL++ feedback for the one-page control and a second valid PDF.

Run from the repository root after `python3 parsarium.py afl build pdf cpp
imagemagick`. Each input is traced twice with afl-showmap; only edge IDs seen
in both runs count, so nondeterministic Ghostscript edges do not inflate the
difference. Writes source-feedback.json next to this script. No campaign or
mutated input is run.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
IMAGE = "parsarium-afl/pdf-cpp-imagemagick:local"
CONTROL = "controls/pdf/one-page.pdf"
VARIANT = "controls/pdf/two-page.pdf"
REPEATS = 2


def trace(receipt: dict, case: Path, work: Path) -> set[str]:
    out = work / "map.txt"
    out.unlink(missing_ok=True)
    subprocess.run([
        "docker", "run", "--rm", "--platform", receipt["platform"],
        "--network", "none", "--read-only", "--cap-drop", "ALL",
        "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}",
        "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", "--workdir", "/tmp",
        "-e", f"AFL_MAP_SIZE={receipt['afl_map_size']}",
        "-v", f"{case}:/input/control:ro", "-v", f"{work}:/out",
        "--entrypoint", "afl-showmap", IMAGE,
        "-q", "-m", "none", "-t", "10000", "-o", "/out/map.txt", "--",
        "/work/fuzzer", "/input/control",
    ], check=True, capture_output=True, text=True)
    return {line.split(":")[0] for line in out.read_text().splitlines() if line}


def main() -> None:
    receipt = json.loads((HERE / "verification.json").read_text())
    image_id = subprocess.run(["docker", "image", "inspect", IMAGE, "--format", "{{.Id}}"],
                              check=True, capture_output=True, text=True).stdout.strip()
    if image_id != receipt["image_id"]:
        raise SystemExit("overlay image differs from verification.json; rebuild first")
    with tempfile.TemporaryDirectory(prefix="parsarium-im-pdf-") as temporary:
        work = Path(temporary)
        runs = {name: [trace(receipt, ROOT / name, work) for _ in range(REPEATS)]
                for name in (CONTROL, VARIANT)}
    stable = {name: set.intersection(*maps) for name, maps in runs.items()}
    control, variant = stable[CONTROL], stable[VARIANT]

    def entry(name: str) -> dict:
        return {"path": name, "sha256": sha256((ROOT / name).read_bytes()).hexdigest(),
                "repeat_edge_counts": [len(m) for m in runs[name]],
                "stable_edges": len(stable[name])}

    report = {"schema_version": 1,
              "engine": f"afl-showmap {receipt['afl_package']}, valid PDFs only, {REPEATS} runs each",
              "command": "afl-showmap -q -m none -t 10000 -o OUTPUT -- /work/fuzzer /input/control",
              "image_id": image_id,
              "control": entry(CONTROL), "valid_variant": entry(VARIANT),
              "shared_edge_ids": len(control & variant),
              "control_only_edge_ids": len(control - variant),
              "variant_only_edge_ids": len(variant - control),
              "mutation_campaign_run": False,
              "pass": bool(control) and bool(variant - control)}
    (HERE / "source-feedback.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report))
    if not report["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
