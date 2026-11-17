"""Check mp3-duration's frame-scanner AFL++ feedback on two untagged MPEG controls."""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import importlib.util
import subprocess
import tempfile

from run_case import ROOT, project_for


REPORT = ROOT / "data/javascript/mp3/mp3_duration-feedback-differential.json"
SPEC = importlib.util.spec_from_file_location("mp3_controls", ROOT / "controls/mp3/check_controls.py")
WALKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WALKER)

def expected_duration(path: Path) -> int:
    info = WALKER.walk(path.read_bytes())
    return round(1000 * info["frames"] * info["samples_per_frame"] / info["sample_rate"])


def parser_call_counts(features: set[str], function: str) -> set[int]:
    marker = f":{function}:"
    return {int(item.rsplit(":hits=", 1)[1]) for item in features if marker in item}


def module_load_baseline(image: str, manifest: dict, work: Path) -> int:
    directory = work / "no-parse"
    directory.mkdir()
    run(["docker", "run", "--rm", "--platform", manifest["platform"],
         "--network", "none", "--read-only", "--cap-drop", "ALL",
         "--security-opt", "no-new-privileges",
         "--user", f"{os.getuid()}:{os.getgid()}",
         "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
         "-e", "NODE_V8_COVERAGE=/coverage",
         "-v", f"{directory}:/coverage", "--entrypoint", "node", image,
         "-e", "require('/work/node_modules/mp3-duration')"])
    functions = set(manifest["afl_js_count_functions"])
    count = 0
    seen_parser_script = False
    for path in directory.glob("coverage-*.json"):
        for script in json.loads(path.read_text())["result"]:
            if not script["url"].endswith("/node_modules/mp3-duration/index.js"):
                continue
            seen_parser_script = True
            count += sum(1 for fn in script["functions"] if fn["functionName"] in functions
                         for item in fn["ranges"] if item["count"] > 0)
    if not seen_parser_script:
        raise RuntimeError("no-parse baseline did not load mp3-duration source")
    return count


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])
    return result.stdout


def sandbox(manifest: dict, case: Path, work: Path) -> list[str]:
    return ["docker", "run", "--rm", "--platform", manifest["platform"],
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
            "-v", f"{case}:/input/case:ro", "-v", f"{work}:/coverage"]


def probe(manifest: dict, image: str, case: Path, work: Path, name: str) -> tuple[set, set]:
    common = sandbox(manifest, case, work)
    run([*common, "--entrypoint", "/bin/sh", image,
         "/work/afl_trace", "/input/case", f"/coverage/{name}.features"])
    run([*common, "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap",
         image, "-m", "none", "-t", "30000", "-o", f"/coverage/{name}.map",
         "--", "/work/afl_proxy", "/input/case"])
    features = set((work / f"{name}.features").read_text().splitlines()) - {""}
    tuples = {line.split(":", 1)[0] for line in (work / f"{name}.map").read_text().splitlines() if line}
    return features, tuples


def main() -> None:
    slug = "mp3_duration"
    project, manifest = project_for("mp3", "javascript", slug)
    relative = Path("mp3/javascript") / slug
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    base = json.loads((project / "verification.json").read_text())
    if receipt["base_image_id"] != base["image_id"]:
        raise ValueError("overlay was built from a different project image")
    control, differential = ROOT / manifest["control"], ROOT / manifest["differential_control"]
    for path, digest in ((control, manifest["control_sha256"]),
                         (differential, manifest["differential_control_sha256"])):
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"control hash mismatch: {path}")
    with tempfile.TemporaryDirectory(prefix="parsarium-mp3-duration-") as temporary:
        work = Path(temporary)
        replay = lambda case: json.loads(run([*sandbox(manifest, case, work), "--entrypoint", "node",
                                              base["image_id"], "/work/replay.js", "/input/case"]))
        observed, replayed = replay(control), replay(differential)
        if observed != manifest["expected_output"] or observed != {"duration_ms": expected_duration(control)}:
            raise RuntimeError(f"first control duration differs from frame walker: {observed}")
        if replayed != manifest["differential_expected_output"] or replayed != {"duration_ms": expected_duration(differential)}:
            raise RuntimeError(f"second control duration differs from frame walker: {replayed}")
        controls = [probe(manifest, receipt["image_id"], control, work, f"control-{i}") for i in range(3)]
        others = [probe(manifest, receipt["image_id"], differential, work, f"other-{i}") for i in range(3)]
        first, other = controls[0], others[0]
        baseline_count = module_load_baseline(receipt["image_id"], manifest, work)
    if baseline_count != 0:
        raise RuntimeError(f"{relative}: no-parse module load executed parser functions")
    if any(item != first for item in controls) or any(item != other for item in others):
        raise RuntimeError(f"{relative}: repeated probe changed parser features or AFL++ map")
    if len(first[0]) != receipt["parser_source_features"] or len(first[1]) != receipt["feedback_edges"]:
        raise RuntimeError(f"{relative}: control probe differs from overlay receipt")
    feature_difference = len(first[0] ^ other[0])
    tuple_difference = len(first[1] ^ other[1])
    if not feature_difference or not tuple_difference:
        raise RuntimeError(f"{relative}: second control did not change parser feedback")
    first_frames = WALKER.walk(control.read_bytes())["frames"]
    other_frames = WALKER.walk(differential.read_bytes())["frames"]
    for function in manifest["afl_js_count_functions"]:
        if first_frames not in parser_call_counts(first[0], function):
            raise RuntimeError(f"{relative}: {function} count does not match first frame walk")
        if other_frames not in parser_call_counts(other[0], function):
            raise RuntimeError(f"{relative}: {function} count does not match second frame walk")
    prefix = manifest.get("afl_coverage_subject_prefix", manifest["coverage_subject_prefix"])
    # The subject prefix is one exact source file, not a directory.
    by_file = lambda items: {Path(prefix).name: len(items)} if items else {}
    result = {"project": str(relative), "pass": True,
              "feedback_kind": receipt["feedback_kind"],
              "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
              "base_image_id": base["image_id"], "overlay_image_id": receipt["image_id"],
              "control": manifest["control"], "control_sha256": manifest["control_sha256"],
              "differential": manifest["differential_control"],
              "differential_sha256": manifest["differential_control_sha256"],
              "differential_output": replayed,
              "repeats_per_control": 3,
              "control_output": observed,
              "control_oracle_duration_ms": expected_duration(control),
              "differential_oracle_duration_ms": expected_duration(differential),
              "no_parse_parser_features": baseline_count,
              "feedback_interpretation": "parser-function source-range hit counts capped at 255; 11 versus 12 frame calls, which can track input length as well as parsing, not new branch or line coverage",
              "control_parser_calls": {name: sorted(parser_call_counts(first[0], name)) for name in manifest["afl_js_count_functions"]},
              "differential_parser_calls": {name: sorted(parser_call_counts(other[0], name)) for name in manifest["afl_js_count_functions"]},
              "repeated_control_identical": True, "repeated_differential_identical": True,
              "control_parser_features": len(first[0]), "control_afl_tuples": len(first[1]),
              "differential_parser_features": len(other[0]), "differential_afl_tuples": len(other[1]),
              "parser_feature_difference": feature_difference, "afl_tuple_difference": tuple_difference,
              "control_only_features_by_file": by_file(first[0] - other[0]),
              "differential_only_features_by_file": by_file(other[0] - first[0]),
              "control_only_features": sorted(first[0] - other[0]),
              "differential_only_features": sorted(other[0] - first[0])}
    results = [result]
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "projects_total": len(results), "projects_passed": len(results),
        "differential_kind": "fixed_valid_mpeg2_stereo_control",
        "standard_feedback": "none: Node.js core ships no MP3 parser API",
        "results": results}, indent=2, ensure_ascii=False) + "\n")
    print(f"{relative}: stable repeats; {feature_difference} parser features, "
          f"{tuple_difference} AFL++ tuples differ", flush=True)


if __name__ == "__main__":
    main()
