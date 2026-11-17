"""Build the mp3/rust/rusty_mp3 AFL++ overlay and check its feedback.

The overlay is the afl.rs build from scripts/build_afl_rust.py, with
SanitizerCoverage limited to the rusty_mp3 crate (manifest key
afl_instrumented_crates; rustc wrapper plus a post-build guard scan). The
harness calls only non-generic Mp3Decoder methods, so the harness, sha2,
serde_json, afl and the afl_fuzzer entry point stay uninstrumented.

This script checks both valid controls' results in the verified base image
against the independent frame-header walk in controls/mp3/check_controls.py,
then runs afl-showmap in REPEATS separate containers per control and requires
byte-identical map files and control-dependent tuples. No mutation campaign
and no malformed input is run.
"""

from hashlib import sha256
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "controls/mp3"))
from build_afl_rust import build_one, command  # noqa: E402
from check_controls import walk  # noqa: E402

FORMAT, ECOSYSTEM, SLUG = "mp3", "rust", "rusty_mp3"
OVERLAY = Path(__file__).resolve().parent
REPEATS = 5
FEEDBACK_SCOPE = ("SanitizerCoverage only in the rusty_mp3 1.0.6 crate's object code (decoder, frame sync, "
                  "header and side-info parsing; the encoder is linked but not reached); the harness, sha2, "
                  "serde_json, afl and the afl_fuzzer entry point are built without coverage")


def oracle(data: bytes) -> dict:
    """Independent expectation from the frame-header walk."""
    header = walk(data)
    return {"sample_rate": header["sample_rate"], "channels": header["channels"], "frames": header["frames"],
            "samples_per_channel": header["frames"] * header["samples_per_frame"],
            "pcm_samples": header["frames"] * header["samples_per_frame"] * header["channels"]}


def docker_base(platform: str) -> list[str]:
    return ["docker", "run", "--rm", "-i", "--platform", platform, "--network", "none",
            "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", "--workdir", "/tmp"]


def showmap(image: str, platform: str, map_size: int, data: bytes) -> bytes:
    """afl-showmap tuple:bucket output for one input in a fresh container."""
    out = OVERLAY / "edges.txt"
    command([*docker_base(platform), "-e", f"AFL_MAP_SIZE={map_size}",
             "-v", f"{OVERLAY}:/coverage", "--entrypoint", "afl-showmap", image,
             "-m", "none", "-t", "10000", "-o", "/coverage/edges.txt", "--", "/work/afl_fuzzer"],
            input_data=data)
    found = out.read_bytes()
    out.unlink()
    return found


def tuples(map_text: bytes) -> set[str]:
    return {line.split(":", 1)[0] for line in map_text.decode().splitlines() if line}


def parser_lines(base_image: str, platform: str, path: Path, prefix: str) -> tuple[dict[str, int], dict[str, set[int]]]:
    """Per file under one crate prefix for one input, from the base image: llvm-cov summary
    covered-line counts and the set of lcov DA lines with a nonzero count."""
    script = ("LLVM_PROFILE_FILE=/tmp/c.profraw /work/replay /input/case >/dev/null"
              " && /work/llvm-profdata merge -sparse /tmp/c.profraw -o /tmp/c.profdata"
              " && /work/llvm-cov export /work/replay -instr-profile=/tmp/c.profdata -summary-only"
              " && echo '#LCOV' && /work/llvm-cov export /work/replay -instr-profile=/tmp/c.profdata -format=lcov")
    run = command([*docker_base(platform), "-v", f"{path}:/input/case:ro",
                   "--entrypoint", "/bin/sh", base_image, "-c", script])
    summary, lcov = run.stdout.decode().split("#LCOV\n", 1)
    files = json.loads(summary)["data"][0]["files"]
    counts = {f["filename"][len(prefix):]: f["summary"]["lines"]["covered"]
              for f in files if f["filename"].startswith(prefix)}
    lines, current = {}, None
    for line in lcov.splitlines():
        if line.startswith("SF:"):
            current = line[3:][len(prefix):] if line[3:].startswith(prefix) else None
            if current is not None:
                lines[current] = set()
        elif line.startswith("DA:") and current is not None:
            number, hits = line[3:].split(",")[:2]
            if int(hits):
                lines[current].add(int(number))
    return counts, lines


def repeat_record(runs: list[bytes]) -> dict:
    return {"repeat_map_sha256": [sha256(run).hexdigest() for run in runs],
            "repeat_tuple_counts": [len(tuples(run)) for run in runs],
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
    outputs, oracles = {}, {}
    for name, key, data in (("control", "control", control), ("variant", "afl_variant", variant)):
        run = command([*docker_base(platform), "-e", "LLVM_PROFILE_FILE=/tmp/replay.profraw",
                       "-v", f"{ROOT / manifest[key]}:/input/case:ro",
                       "--entrypoint", "/work/replay", base_image, "/input/case"])
        outputs[name] = json.loads(run.stdout)
        oracles[name] = oracle(data)
        if any(outputs[name].get(field) != value for field, value in oracles[name].items()):
            raise RuntimeError(f"{name} disagrees with the header-walk oracle: {outputs[name]} {oracles[name]}")
    if outputs["control"] != manifest["expected_output"]:
        raise RuntimeError(f"control mismatch: {outputs['control']}")
    if outputs["variant"] != manifest["afl_variant_expected_output"]:
        raise RuntimeError(f"second control mismatch: {outputs['variant']}")
    scope = json.loads(command(["docker", "run", "--rm", "--platform", platform, "--entrypoint", "cat",
                                image, "/work/sancov-scope.json"]).stdout)
    scope_log = command(["docker", "run", "--rm", "--platform", platform, "--entrypoint", "cat",
                         image, "/work/sancov-scope.log"]).stdout.decode().split("\n")
    instrumented = sorted({line.split()[1] for line in scope_log if line.startswith("instrumented ")})
    if instrumented != sorted(manifest["afl_instrumented_crates"]) or scope["instrumented_crates"] != instrumented:
        raise RuntimeError(f"unexpected instrumentation scope: {instrumented} {scope}")
    map_size = receipt["afl_map_size"]
    control_runs = [showmap(image, platform, map_size, control) for _ in range(REPEATS)]
    variant_runs = [showmap(image, platform, map_size, variant) for _ in range(REPEATS)]
    if any(run != control_runs[0] for run in control_runs) or any(run != variant_runs[0] for run in variant_runs):
        raise RuntimeError("AFL++ maps differ between separate processes on the same control")
    control_tuples, variant_tuples = tuples(control_runs[0]), tuples(variant_runs[0])
    if not control_tuples or not variant_tuples:
        raise RuntimeError("a valid control produced no feedback")
    if not (control_tuples - variant_tuples) or not (variant_tuples - control_tuples):
        raise RuntimeError("AFL++ feedback does not depend on the control")
    differentials = {}
    prefixes = [("own", manifest["coverage_subject_prefix"])]
    if "underlying_coverage_subject_prefix" in manifest:
        prefixes.append(("underlying", manifest["underlying_coverage_subject_prefix"]))
    for key, prefix in prefixes:
        control_lines, control_set = parser_lines(base_image, platform, ROOT / manifest["control"], prefix)
        variant_lines, variant_set = parser_lines(base_image, platform, ROOT / manifest["afl_variant"], prefix)
        if not sum(control_lines.values()) or not sum(variant_lines.values()):
            raise RuntimeError(f"no {key} source lines covered by a valid control")
        differentials[key] = {
            "prefix": prefix, "control_lines": control_lines, "variant_lines": variant_lines,
            "files_with_different_line_counts": sorted(name for name in control_lines
                if control_lines[name] != variant_lines.get(name)),
            "line_set_rule": "lcov DA lines with a nonzero count under the prefix",
            "lines_only_in_control": {name: sorted(control_set[name] - variant_set.get(name, set()))
                                      for name in sorted(control_set)
                                      if control_set[name] - variant_set.get(name, set())},
            "lines_only_in_variant": {name: sorted(variant_set[name] - control_set.get(name, set()))
                                      for name in sorted(variant_set)
                                      if variant_set[name] - control_set.get(name, set())},
        }
    parser_key = prefixes[-1][0]
    if not (differentials[parser_key]["lines_only_in_control"] and differentials[parser_key]["lines_only_in_variant"]):
        raise RuntimeError("parser source lines do not depend on the control")
    afl_version = command(["docker", "run", "--rm", "--platform", platform, "--entrypoint", "dpkg-query",
                           image, "-W", "-f=${Version}", "afl++"]).stdout.decode().strip()
    receipt.update({
        "feedback_kind": "afl_rs_rust_sancov_edges",
        "feedback_scope": FEEDBACK_SCOPE,
        "sancov_scope": scope,
        "rustc_wrapper_log": sorted(line for line in scope_log if line),
        "afl_version_output": afl_version,
        "base_image_id": base_id,
        "variant_sha256": manifest["afl_variant_sha256"],
        "control_output": outputs["control"], "variant_output": outputs["variant"],
        "header_walk_oracle": {"script": "controls/mp3/check_controls.py",
                               "control": oracles["control"], "variant": oracles["variant"]},
        "repeats": REPEATS,
        "repeat_rule": "each repeat is a separate docker run of afl-showmap; map files (tuple:bucket) must be byte-identical",
        "feedback_edges": len(control_tuples),
        "variant_feedback_edges": len(variant_tuples),
        "control_map_sha256": sha256(control_runs[0]).hexdigest(),
        "variant_map_sha256": sha256(variant_runs[0]).hexdigest(),
        "edges_only_in_control": len(control_tuples - variant_tuples),
        "edges_only_in_variant": len(variant_tuples - control_tuples),
        "own_source_differential": differentials["own"],
        "mutation_campaign_run": False,
        "control_stability": repeat_record(control_runs),
        "variant_stability": repeat_record(variant_runs),
    })
    if "underlying" in differentials:
        receipt.update({"underlying_source_differential": differentials["underlying"],
                        "underlying_package": manifest["underlying_package"],
                        "underlying_source_sha256": manifest["underlying_source_sha256"]})
    receipt["overlay_file_sha256"]["build.py"] = sha256(Path(__file__).read_bytes()).hexdigest()
    (OVERLAY / "verification.json").write_text(json.dumps(receipt, indent=2) + "\n")
    print(f"Verified {FORMAT}/{ECOSYSTEM}/{SLUG}: {len(control_tuples)} control and "
          f"{len(variant_tuples)} second-control AFL++ tuples, identical over {REPEATS} processes each")


if __name__ == "__main__":
    main()
