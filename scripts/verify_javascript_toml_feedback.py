"""Check the JavaScript TOML AFL++ bridge: both valid TOML controls replay to their pinned
typed trees with per-file parser-source line coverage, three repeated probes of each control
give identical parser features and AFL++ maps, and the two controls differ in both."""

import argparse
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import tempfile

from run_case import ROOT, project_for


SLUGS = ("smol_toml", "toml_eslint_parser", "ltd_j_toml", "decimalturn_toml_patch", "effected_toml", "sgarciac_bombadil")
REPORT = ROOT / "data/javascript/toml/afl-feedback.json"
REPEATS = 3


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])
    return result.stdout


def sandbox(manifest: dict, case: Path, work: Path, target: str = "/input/case") -> list[str]:
    return ["docker", "run", "--rm", "--platform", manifest["platform"],
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
            "-v", f"{case}:{target}:ro", "-v", f"{work}:/coverage"]


def probe(manifest: dict, image: str, case: Path, work: Path, name: str) -> tuple[frozenset, frozenset]:
    common = sandbox(manifest, case, work)
    run([*common, "--entrypoint", "/bin/sh", image,
         "/work/afl_trace", "/input/case", f"/coverage/{name}.features"])
    run([*common, "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap",
         image, "-m", "none", "-t", "30000", "-o", f"/coverage/{name}.map",
         "--", "/work/afl_proxy", "/input/case"])
    features = frozenset((work / f"{name}.features").read_text().splitlines()) - {""}
    tuples = frozenset(line.split(":", 1)[0] for line in (work / f"{name}.map").read_text().splitlines() if line)
    return features, tuples


def line_coverage(manifest: dict, image: str, case: Path, expected: dict) -> dict:
    """Run the project's run-control on one control; return its per-file covered lines."""
    with tempfile.TemporaryDirectory(prefix="parsarium-toml-js-lines-") as temporary:
        work = Path(temporary)
        summary = json.loads(run([*sandbox(manifest, case, work, "/input/control"), image]).strip().splitlines()[-1])
        if not summary["control_pass"] or summary["output"] != expected:
            raise RuntimeError(f"{case.name}: typed tree differs from the pinned tree")
        files = json.loads((work / "coverage.json").read_text())["data"][0]["files"]
    prefix = manifest["coverage_subject_prefix"]
    return {item["filename"].removeprefix(prefix): item["executed_lines"] for item in files
            if item["filename"].startswith(prefix)}


def verify_project(slug: str) -> dict:
    project, manifest = project_for("toml", "javascript", slug)
    relative = Path("toml/javascript") / slug
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    base = json.loads((project / "verification.json").read_text())
    if receipt["base_image_id"] != base["image_id"]:
        raise ValueError("overlay was built from a different project image")
    if receipt["base_project_receipt_sha256"] != sha256((project / "verification.json").read_bytes()).hexdigest():
        raise ValueError("overlay receipt does not pin the current project receipt")
    control, differential = ROOT / manifest["control"], ROOT / manifest["differential_control"]
    for path, digest in ((control, manifest["control_sha256"]),
                         (differential, manifest["differential_control_sha256"])):
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"control hash mismatch: {path}")
    lines = {"control": line_coverage(manifest, base["image_id"], control, manifest["expected_output"]),
             "differential": line_coverage(manifest, base["image_id"], differential,
                                           manifest["differential_expected_output"])}
    with tempfile.TemporaryDirectory(prefix="parsarium-toml-js-") as temporary:
        work = Path(temporary)
        replayed = json.loads(run([*sandbox(manifest, differential, work), "--entrypoint", "node",
                                   base["image_id"], "/work/replay.js", "/input/case"]))
        if replayed != manifest["differential_expected_output"]:
            raise RuntimeError(f"second control typed tree differs: {replayed}")
        first = [probe(manifest, receipt["image_id"], control, work, f"control-{n}") for n in range(REPEATS)]
        other = [probe(manifest, receipt["image_id"], differential, work, f"differential-{n}")
                 for n in range(REPEATS)]
    if len(set(first)) != 1 or len(set(other)) != 1:
        raise RuntimeError(f"{relative}: repeated probe changed parser features or AFL++ map")
    (control_features, control_tuples), (other_features, other_tuples) = first[0], other[0]
    if len(control_features) != receipt["parser_source_features"] or len(control_tuples) != receipt["feedback_edges"]:
        raise RuntimeError(f"{relative}: control probe differs from overlay receipt")
    feature_difference = len(control_features ^ other_features)
    tuple_difference = len(control_tuples ^ other_tuples)
    if feature_difference < 2 or tuple_difference < 2:
        raise RuntimeError(f"{relative}: second control did not change parser feedback by at least 2")
    prefix = manifest["coverage_subject_prefix"]

    def by_file(items: frozenset) -> dict:
        counts: dict[str, int] = {}
        for item in items:
            name = item[len(prefix):].rsplit(":", 1)[0]
            counts[name] = counts.get(name, 0) + 1
        return dict(sorted(counts.items()))

    def line_counts(which: str) -> dict:
        return {name: len(executed) for name, executed in sorted(lines[which].items())}

    def line_only(which: str, against: str) -> dict:
        result = {name: len(set(executed) - set(lines[against].get(name, [])))
                  for name, executed in sorted(lines[which].items())}
        return {name: count for name, count in result.items() if count}

    result = {"project": str(relative), "pass": True,
              "feedback_kind": receipt["feedback_kind"],
              "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
              "base_project_receipt_sha256": receipt["base_project_receipt_sha256"],
              "base_image_id": base["image_id"], "overlay_image_id": receipt["image_id"],
              "control": manifest["control"], "control_sha256": manifest["control_sha256"],
              "differential": manifest["differential_control"],
              "differential_sha256": manifest["differential_control_sha256"],
              "differential_output_matches_expected": True,
              "repeats_per_control": REPEATS,
              "repeated_control_identical": True, "repeated_differential_identical": True,
              "control_parser_features": len(control_features), "control_afl_tuples": len(control_tuples),
              "differential_parser_features": len(other_features),
              "differential_afl_tuples": len(other_tuples),
              "parser_feature_difference": feature_difference, "afl_tuple_difference": tuple_difference,
              "control_only_afl_tuples": len(control_tuples - other_tuples),
              "differential_only_afl_tuples": len(other_tuples - control_tuples),
              "control_only_features_by_file": by_file(control_features - other_features),
              "differential_only_features_by_file": by_file(other_features - control_features),
              "control_parser_source_lines_by_file": line_counts("control"),
              "differential_parser_source_lines_by_file": line_counts("differential"),
              "control_only_parser_source_lines_by_file": line_only("control", "differential"),
              "differential_only_parser_source_lines_by_file": line_only("differential", "control")}
    print(f"{relative}: {REPEATS} identical repeats per control; {feature_difference} parser features, "
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
    results = [results_by_slug[slug] for slug in SLUGS if slug in results_by_slug]
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "projects_total": len(results), "projects_passed": sum(item["pass"] for item in results),
        "differential_kind": "fixed_valid_typed_scalars",
        "results": results}, indent=2, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    main()
