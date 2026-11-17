"""Build the json/rust/json_crate AFL++ overlay and check its feedback.

The overlay is the standard afl.rs build from scripts/build_afl_rust.py. This
script adds a fixed second valid control: it checks that control's parsed
result in the verified base image, then runs afl-showmap three times on each
control. The receipt records edge counts, stability, and the edges unique to
each control. No mutation campaign and no malformed input is run.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "scripts"))
from build_afl_rust import build_one, command  # noqa: E402

FORMAT, ECOSYSTEM, SLUG = "json", "rust", "json_crate"
OVERLAY = Path(__file__).resolve().parent
REPEATS = 3


def docker_base(platform: str) -> list[str]:
    return ["docker", "run", "--rm", "-i", "--platform", platform, "--network", "none",
            "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", "--workdir", "/tmp"]


def edges(image: str, platform: str, map_size: int, data: bytes) -> set[str]:
    out = OVERLAY / "edges.txt"
    command([*docker_base(platform), "-e", f"AFL_MAP_SIZE={map_size}",
             "-v", f"{OVERLAY}:/coverage", "--entrypoint", "afl-showmap", image,
             "-m", "none", "-t", "10000", "-o", "/coverage/edges.txt", "--", "/work/afl_fuzzer"],
            input_data=data)
    found = {line.split(":", 1)[0] for line in out.read_text().splitlines() if line}
    out.unlink()
    return found


def parser_lines(base_image: str, platform: str, path: Path, prefix: str) -> dict[str, int]:
    """Covered json source lines per file for one input, from the base image."""
    script = ("LLVM_PROFILE_FILE=/tmp/c.profraw /work/replay /input/case >/dev/null"
              " && /work/llvm-profdata merge -sparse /tmp/c.profraw -o /tmp/c.profdata"
              " && /work/llvm-cov export /work/replay -instr-profile=/tmp/c.profdata -summary-only")
    run = command([*docker_base(platform), "-v", f"{path}:/input/case:ro",
                   "--entrypoint", "/bin/sh", base_image, "-c", script])
    files = json.loads(run.stdout)["data"][0]["files"]
    return {f["filename"][len(prefix):]: f["summary"]["lines"]["covered"]
            for f in files if f["filename"].startswith(prefix)}


def stability(runs: list[set[str]]) -> dict:
    stable, union = set.intersection(*runs), set.union(*runs)
    return {"repeat_edge_counts": [len(run) for run in runs], "stable_edges": len(stable),
            "union_edges": len(union), "stable_ratio": round(len(stable) / len(union), 6),
            "all_repeats_identical": all(run == runs[0] for run in runs)}


def main() -> None:
    receipt = build_one(FORMAT, ECOSYSTEM, SLUG)
    manifest = json.loads((ROOT / "projects" / FORMAT / ECOSYSTEM / SLUG / "manifest.json").read_text())
    platform, image = manifest["platform"], f"parsarium-afl/{FORMAT}-{ECOSYSTEM}-{SLUG}:local"
    control = (ROOT / manifest["control"]).read_bytes()
    variant = (ROOT / manifest["afl_variant"]).read_bytes()
    if sha256(variant).hexdigest() != manifest["afl_variant_sha256"]:
        raise RuntimeError("second control changed")
    base_image = f"parsarium/{FORMAT}-{ECOSYSTEM}-{SLUG}:local"
    base_id = command(["docker", "image", "inspect", base_image, "--format", "{{.Id}}"]).stdout.decode().strip()
    project_receipt = json.loads((ROOT / "projects" / FORMAT / ECOSYSTEM / SLUG / "verification.json").read_text())
    if base_id != project_receipt["image_id"]:
        raise RuntimeError("base image differs from the project receipt; run parsarium.py build first")
    outputs = {}
    for name, data in (("control", control), ("variant", variant)):
        run = command([*docker_base(platform), "-e", "LLVM_PROFILE_FILE=/tmp/replay.profraw",
                       "-v", f"{ROOT / manifest[name if name == 'control' else 'afl_variant']}:/input/case:ro",
                       "--entrypoint", "/work/replay", base_image, "/input/case"])
        outputs[name] = json.loads(run.stdout)
    if outputs["control"] != manifest["expected_output"]:
        raise RuntimeError(f"control mismatch: {outputs['control']}")
    if outputs["variant"] != manifest["afl_variant_expected_output"]:
        raise RuntimeError(f"second control mismatch: {outputs['variant']}")
    map_size = receipt["afl_map_size"]
    control_runs = [edges(image, platform, map_size, control) for _ in range(REPEATS)]
    variant_runs = [edges(image, platform, map_size, variant) for _ in range(REPEATS)]
    control_stable, variant_stable = set.intersection(*control_runs), set.intersection(*variant_runs)
    if not control_stable or not variant_stable:
        raise RuntimeError("a valid control produced no stable feedback")
    prefix = manifest["coverage_subject_prefix"]
    control_lines = parser_lines(base_image, platform, ROOT / manifest["control"], prefix)
    variant_lines = parser_lines(base_image, platform, ROOT / manifest["afl_variant"], prefix)
    if not sum(control_lines.values()) or not sum(variant_lines.values()):
        raise RuntimeError("no parser source lines covered by a valid control")
    differing = sorted(name for name in control_lines
                       if control_lines[name] != variant_lines.get(name))
    if "src/parser.rs" not in differing:
        raise RuntimeError("valid controls did not yield differential json-rust parser source coverage")
    afl_version = command(["docker", "run", "--rm", "--platform", platform, "--entrypoint", "dpkg-query",
                           image, "-W", "-f=${Version}", "afl++"]).stdout.decode().strip()
    receipt.update({
        "feedback_kind": "afl_rs_rust_sancov_edges",
        "feedback_scope": "Whole afl_fuzzer binary built by cargo-afl: json-rust 0.12.4 parser, serde_json summary serializer, their dependencies and the harness are instrumented",
        "afl_version_output": afl_version,
        "base_image_id": base_id,
        "variant_sha256": manifest["afl_variant_sha256"],
        "control_output": outputs["control"], "variant_output": outputs["variant"],
        "repeats": REPEATS,
        "feedback_edges": len(control_stable),
        "variant_feedback_edges": len(variant_stable),
        "edges_only_in_control": len(control_stable - variant_stable),
        "edges_only_in_variant": len(variant_stable - control_stable),
        "source_differential": {
            "parser_prefix": prefix,
            "control_lines": control_lines, "variant_lines": variant_lines,
            "files_with_different_line_counts": differing,
        },
        "control_stability": stability(control_runs),
        "variant_stability": stability(variant_runs),
    })
    receipt["overlay_file_sha256"]["build.py"] = sha256(Path(__file__).read_bytes()).hexdigest()
    (OVERLAY / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"Verified {FORMAT}/{ECOSYSTEM}/{SLUG}: {len(control_stable)} control and "
          f"{len(variant_stable)} second-control AFL++ edges over {REPEATS} repeats")


if __name__ == "__main__":
    main()
