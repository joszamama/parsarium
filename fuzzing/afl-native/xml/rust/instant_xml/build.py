"""Build the xml/rust/instant_xml AFL++ overlay and check its feedback.

The overlay is the standard afl.rs build from scripts/build_afl_rust.py with
SanitizerCoverage restricted to instant-xml and the xmlparser tokenizer it
drives. This script checks both valid controls in the verified base image,
records the shared order control's rejection, then runs afl-showmap ten times
on each control. instant-xml rejects a processing instruction inside the root,
so the second control is order-default-ns-no-pi.xml. The receipt records edge
counts, stability, the edges unique to each control, and per-file instant-xml
and xmlparser source lines. No mutation campaign and no malformed input is run.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "scripts"))
from build_afl_rust import build_one, command  # noqa: E402

FORMAT, ECOSYSTEM, SLUG = "xml", "rust", "instant_xml"
OVERLAY = Path(__file__).resolve().parent
REPEATS = 10
CRATES = ["instant_xml", "xmlparser"]


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


def source_lines(base_image: str, platform: str, path: Path, prefixes: list[str]) -> list[dict[str, int]]:
    """Covered source lines per file under each prefix for one input, from the base image."""
    script = ("LLVM_PROFILE_FILE=/tmp/c.profraw /work/replay /input/case >/dev/null"
              " && /work/llvm-profdata merge -sparse /tmp/c.profraw -o /tmp/c.profdata"
              " && /work/llvm-cov export /work/replay -instr-profile=/tmp/c.profdata -summary-only")
    run = command([*docker_base(platform), "-v", f"{path}:/input/case:ro",
                   "--entrypoint", "/bin/sh", base_image, "-c", script])
    files = json.loads(run.stdout)["data"][0]["files"]
    return [{f["filename"][len(prefix):]: f["summary"]["lines"]["covered"]
             for f in files if f["filename"].startswith(prefix)} for prefix in prefixes]


def stability(runs: list[set[str]]) -> dict:
    stable, union = set.intersection(*runs), set.union(*runs)
    return {"repeat_edge_counts": [len(run) for run in runs], "stable_edges": len(stable),
            "union_edges": len(union), "stable_ratio": round(len(stable) / len(union), 6),
            "all_repeats_identical": all(run == runs[0] for run in runs)}


def main() -> None:
    receipt = build_one(FORMAT, ECOSYSTEM, SLUG)
    manifest = json.loads((ROOT / "projects" / FORMAT / ECOSYSTEM / SLUG / "manifest.json").read_text())
    platform, image = manifest["platform"], f"parsarium-afl/{FORMAT}-{ECOSYSTEM}-{SLUG}:local"
    if manifest.get("afl_instrumented_crates") != CRATES:
        raise RuntimeError(f"AFL++ target must instrument only {CRATES}")
    scope = json.loads(command(["docker", "run", "--rm", "--platform", platform,
                                "--entrypoint", "cat", image,
                                "/work/sancov-scope.json"]).stdout)
    if scope["instrumented_crates"] != CRATES or set(scope["rlib_guard_bytes"]) != set(CRATES):
        raise RuntimeError(f"SanitizerCoverage is not restricted to instant-xml and xmlparser: {scope}")
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
    for name in ("control", "afl_variant", "shared_second_control"):
        run = command([*docker_base(platform), "-e", "LLVM_PROFILE_FILE=/tmp/replay.profraw",
                       "-v", f"{ROOT / manifest[name]}:/input/case:ro",
                       "--entrypoint", "/work/replay", base_image, "/input/case"],
                      allow_failure=name == "shared_second_control")
        outputs[name] = (json.loads(run.stdout) if not run.returncode
                         else run.stderr.decode(errors="replace").strip().removeprefix("Error: "))
    if outputs["control"] != manifest["expected_output"]:
        raise RuntimeError(f"control mismatch: {outputs['control']}")
    if outputs["afl_variant"] != manifest["afl_variant_expected_output"]:
        raise RuntimeError(f"second control mismatch: {outputs['afl_variant']}")
    if outputs["shared_second_control"] != manifest["shared_second_control_result"]:
        raise RuntimeError(f"shared order control result changed: {outputs['shared_second_control']}")
    map_size = receipt["afl_map_size"]
    control_runs = [edges(image, platform, map_size, control) for _ in range(REPEATS)]
    variant_runs = [edges(image, platform, map_size, variant) for _ in range(REPEATS)]
    control_stable, variant_stable = set.intersection(*control_runs), set.intersection(*variant_runs)
    if not control_stable or not variant_stable:
        raise RuntimeError("a valid control produced no stable feedback")
    if any(run != control_runs[0] for run in control_runs) or any(run != variant_runs[0] for run in variant_runs):
        raise RuntimeError("afl-showmap repeats differ")
    if control_stable == variant_stable:
        raise RuntimeError("valid controls gave identical feedback")
    prefixes = [manifest["coverage_subject_prefix"], manifest["underlying_coverage_subject_prefix"]]
    control_own, control_xp = source_lines(base_image, platform, ROOT / manifest["control"], prefixes)
    variant_own, variant_xp = source_lines(base_image, platform, ROOT / manifest["afl_variant"], prefixes)
    if not sum(control_own.values()) or not sum(variant_own.values()):
        raise RuntimeError("no instant-xml source lines covered by a valid control")
    differing_own = sorted(name for name in control_own if control_own[name] != variant_own.get(name))
    differing_xp = sorted(name for name in control_xp if control_xp[name] != variant_xp.get(name))
    if not differing_own and not differing_xp:
        raise RuntimeError("valid controls did not yield differential instant-xml/xmlparser source coverage")
    afl_version = command(["docker", "run", "--rm", "--platform", platform, "--entrypoint", "dpkg-query",
                           image, "-W", "-f=${Version}", "afl++"]).stdout.decode().strip()
    receipt.update({
        "feedback_kind": "afl_rs_instant_xml_xmlparser_only_sancov_edges",
        "feedback_scope": ("Only instant_xml and xmlparser crate objects carry SanitizerCoverage guards; "
                           "harness, serde_json, the instant-xml-macros proc-macro, AFL runtime and other "
                           "crates are uninstrumented"),
        "sancov_scope": scope,
        "afl_version_output": afl_version,
        "base_image_id": base_id,
        "variant_sha256": manifest["afl_variant_sha256"],
        "control_output": outputs["control"], "variant_output": outputs["afl_variant"],
        "shared_second_control_result": outputs["shared_second_control"],
        "repeats": REPEATS,
        "feedback_edges": len(control_stable),
        "variant_feedback_edges": len(variant_stable),
        "edges_only_in_control": len(control_stable - variant_stable),
        "edges_only_in_variant": len(variant_stable - control_stable),
        "source_differential": {
            "parser_prefix": prefixes[0], "underlying_prefix": prefixes[1],
            "control_lines": control_own, "variant_lines": variant_own,
            "control_underlying_lines": control_xp, "variant_underlying_lines": variant_xp,
            "files_with_different_line_counts": differing_own,
            "underlying_files_with_different_line_counts": differing_xp,
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
