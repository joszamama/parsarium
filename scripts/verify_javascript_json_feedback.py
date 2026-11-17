"""Check the JavaScript JSON AFL++ bridge: the second valid control replays to its pinned
output, repeated probes match, and the second control changes parser feedback."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

from run_case import ROOT, project_for


SLUGS = ("stream_json", "bfj", "streamparser_json")
REPORT = ROOT / "data/javascript/json/afl-feedback.json"


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


def verify_project(slug: str) -> dict:
    project, manifest = project_for("json", "javascript", slug)
    relative = Path("json/javascript") / slug
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
    with tempfile.TemporaryDirectory(prefix="parsarium-json-js-") as temporary:
        work = Path(temporary)
        replayed = json.loads(run([*sandbox(manifest, differential, work), "--entrypoint", "node",
                                   base["image_id"], "/work/replay.js", "/input/case"]))
        if replayed != manifest["differential_expected_output"]:
            raise RuntimeError(f"second control output differs: {replayed}")
        first = probe(manifest, receipt["image_id"], control, work, "first")
        repeat = probe(manifest, receipt["image_id"], control, work, "repeat")
        other = probe(manifest, receipt["image_id"], differential, work, "other")
        other_repeat = probe(manifest, receipt["image_id"], differential, work, "other-repeat")
    if first != repeat or other != other_repeat:
        raise RuntimeError(f"{relative}: repeated probe changed parser features or AFL++ map")
    if len(first[0]) != receipt["parser_source_features"] or len(first[1]) != receipt["feedback_edges"]:
        raise RuntimeError(f"{relative}: control probe differs from overlay receipt")
    feature_difference = len(first[0] ^ other[0])
    tuple_difference = len(first[1] ^ other[1])
    if not feature_difference or not tuple_difference:
        raise RuntimeError(f"{relative}: second control did not change parser feedback")
    prefix = manifest["coverage_subject_prefix"]
    by_file = lambda items: dict(sorted({name: sum(1 for item in items if item.startswith(prefix + name + ":"))
                                         for name in {item[len(prefix):].rsplit(":", 1)[0] for item in items}}.items()))
    result = {"project": str(relative), "pass": True,
              "feedback_kind": receipt["feedback_kind"],
              "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
              "base_image_id": base["image_id"], "overlay_image_id": receipt["image_id"],
              "control": manifest["control"], "control_sha256": manifest["control_sha256"],
              "differential": manifest["differential_control"],
              "differential_sha256": manifest["differential_control_sha256"],
              "differential_output": replayed,
              "repeated_control_identical": True, "repeated_differential_identical": True,
              "control_parser_features": len(first[0]), "control_afl_tuples": len(first[1]),
              "differential_parser_features": len(other[0]), "differential_afl_tuples": len(other[1]),
              "parser_feature_difference": feature_difference, "afl_tuple_difference": tuple_difference,
              "control_only_features_by_file": by_file(first[0] - other[0]),
              "differential_only_features_by_file": by_file(other[0] - first[0])}
    print(f"{relative}: stable repeats; {feature_difference} parser features, "
          f"{tuple_difference} AFL++ tuples differ", flush=True)
    return result


def main() -> None:
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--project", choices=SLUGS, help="refresh one project and retain other pinned results")
    args = cli.parse_args()
    checked = (args.project,) if args.project else SLUGS
    results_by_slug = {}
    if args.project and REPORT.is_file():
        for item in json.loads(REPORT.read_text()).get("results", []):
            results_by_slug[Path(item["project"]).name] = item
    for slug in checked:
        results_by_slug[slug] = verify_project(slug)
    results = [results_by_slug[slug] for slug in SLUGS]
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "projects_total": len(results), "projects_passed": len(results),
        "differential_kind": "fixed_valid_nested_array",
        "standard_feedback": "JSON.parse has staged native function-entry feedback, not JavaScript source ranges",
        "results": results}, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
