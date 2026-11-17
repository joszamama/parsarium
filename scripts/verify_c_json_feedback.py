"""Check the C JSON AFL++ overlay: both valid controls replay to their pinned outputs and
exact nested structure, repeated probes match, and the second control changes feedback.

Parser features are covered LLVM region entries inside the pinned jansson source tree
(the harness is excluded). AFL++ tuples come from afl-showmap on the overlay fuzzer.
"""

from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

from run_case import ROOT, project_for


SLUG = "jansson"
REPORT = ROOT / "data/c/json/afl-feedback.json"
REPEATS = 2


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])
    return result.stdout


def sandbox(manifest: dict, case: Path, work: Path) -> list[str]:
    return ["docker", "run", "--rm", "--platform", manifest["platform"],
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", "--workdir", "/tmp",
            "-v", f"{case}:/input/case:ro", "-v", f"{work}:/coverage"]


def typed(value):
    if isinstance(value, list):
        return [typed(item) for item in value]
    if isinstance(value, tuple):
        return (value[0], typed(value[1]))
    return (type(value).__name__, value)


def replay(manifest: dict, image: str, case: Path, work: Path) -> dict:
    common = sandbox(manifest, case, work)
    summary = json.loads(run([*common, "-e", "LLVM_PROFILE_FILE=/tmp/x.profraw",
                              "--entrypoint", "/work/replay", image, "/input/case"]))
    tree = run([*common, "-e", "LLVM_PROFILE_FILE=/tmp/x.profraw",
                "--entrypoint", "/work/replay", image, "/input/case", "--tree"])
    if typed(json.loads(tree, object_pairs_hook=list)) != typed(
            json.loads(case.read_text(), object_pairs_hook=list)):
        raise RuntimeError(f"{case.name}: parsed tree differs from exact nested structure")
    return summary


def features(manifest: dict, image: str, case: Path, work: Path, name: str) -> set[str]:
    common = sandbox(manifest, case, work)
    script = (f"LLVM_PROFILE_FILE=/coverage/{name}.profraw /work/replay /input/case > /dev/null && "
              f"llvm-profdata merge -sparse /coverage/{name}.profraw -o /coverage/{name}.profdata && "
              f"llvm-cov export /work/replay -instr-profile=/coverage/{name}.profdata "
              f"> /coverage/{name}.coverage.json")
    run([*common, "--entrypoint", "/bin/sh", image, "-c", script])
    coverage = json.loads((work / f"{name}.coverage.json").read_text())
    prefix = manifest["coverage_subject_prefix"]
    return {f"{item['filename']}:{line}:{column}"
            for item in coverage["data"][0]["files"] if item["filename"].startswith(prefix)
            for line, column, count, has_count, entry, gap in item["segments"]
            if has_count and entry and not gap and count > 0}


def tuples(manifest: dict, image: str, case: Path, work: Path, name: str, map_size: int) -> set[str]:
    run([*sandbox(manifest, case, work), "-e", f"AFL_MAP_SIZE={map_size}",
         "--entrypoint", "afl-showmap", image, "-m", "none", "-t", "10000",
         "-o", f"/coverage/{name}.map", "--", "/work/fuzzer", "/input/case"])
    return {line.split(":", 1)[0] for line in (work / f"{name}.map").read_text().splitlines() if line}


def main() -> None:
    project, manifest = project_for("json", "c", SLUG)
    relative = Path("json/c") / SLUG
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    base = json.loads((project / "verification.json").read_text())
    if receipt["base_project_receipt_sha256"] != sha256((project / "verification.json").read_bytes()).hexdigest():
        raise ValueError("overlay was built against a different project receipt")
    base_image = run(["docker", "image", "inspect", f"parsarium/json-c-{SLUG}:local",
                      "--format", "{{.Id}}"]).strip()
    if base_image != base["image_id"]:
        raise ValueError("local project image differs from its receipt")
    controls = [ROOT / manifest["control"], ROOT / manifest["differential_control"]]
    digests = [manifest["control_sha256"], manifest["differential_control_sha256"]]
    for path, digest in zip(controls, digests):
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"control hash mismatch: {path}")
    with tempfile.TemporaryDirectory(prefix="parsarium-json-c-") as temporary:
        work = Path(temporary)
        outputs = [replay(manifest, base_image, path, work) for path in controls]
        if outputs != [manifest["expected_output"], manifest["differential_expected_output"]]:
            raise RuntimeError(f"control outputs differ: {outputs}")
        observed = []
        for index, control in enumerate(controls):
            runs = [(features(manifest, base_image, control, work, f"{index}-{attempt}"),
                     tuples(manifest, receipt["image_id"], control, work, f"{index}-{attempt}",
                            receipt["afl_map_size"]))
                    for attempt in range(REPEATS)]
            if any(item != runs[0] for item in runs):
                raise RuntimeError(f"{control.name}: repeated probe changed parser features or AFL++ map")
            observed.append(runs[0])
    first, other = observed
    if len(first[1]) != receipt["feedback_edges"]:
        raise RuntimeError(f"{relative}: control probe differs from overlay receipt")
    feature_difference = len(first[0] ^ other[0])
    tuple_difference = len(first[1] ^ other[1])
    if not feature_difference or not tuple_difference:
        raise RuntimeError(f"{relative}: second control did not change parser feedback")
    prefix = manifest["coverage_subject_prefix"]
    by_file = lambda items: dict(sorted(Counter(
        item.removeprefix(prefix).rsplit(":", 2)[0] for item in items).items()))
    result = {"project": str(relative), "pass": True,
              "feedback_kind": "c_llvm_parser_regions_and_afl_native_edges",
              "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
              "base_image_id": base_image, "overlay_image_id": receipt["image_id"],
              "control": manifest["control"], "control_sha256": digests[0],
              "differential": manifest["differential_control"], "differential_sha256": digests[1],
              "differential_output": outputs[1],
              "exact_nested_structure_match": True,
              "repeats_per_control": REPEATS,
              "repeated_control_identical": True, "repeated_differential_identical": True,
              "control_parser_features": len(first[0]), "control_afl_tuples": len(first[1]),
              "differential_parser_features": len(other[0]), "differential_afl_tuples": len(other[1]),
              "parser_feature_difference": feature_difference, "afl_tuple_difference": tuple_difference,
              "control_only_features_by_file": by_file(first[0] - other[0]),
              "differential_only_features_by_file": by_file(other[0] - first[0])}
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "projects_total": 1, "projects_passed": 1,
        "differential_kind": "fixed_valid_nested_array",
        "parser_feature_scope": "covered LLVM region entries under the pinned jansson source prefix; harness excluded",
        "afl_feedback_scope": "afl-clang-fast edges over jansson src/*.c and the harness; the AFL++ map is not split by file",
        "standard_feedback": "none: the ISO C standard library documents no JSON API",
        "results": [result]}, indent=2, ensure_ascii=False) + "\n")
    print(f"{relative}: stable repeats; {feature_difference} parser features, "
          f"{tuple_difference} AFL++ tuples differ", flush=True)


if __name__ == "__main__":
    main()
