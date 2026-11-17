"""Check Go TOML AFL++ bridges: both valid controls pass, repeat identically and give different feedback."""

from collections import defaultdict
from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from run_case import ROOT, project_for


PROJECTS = ("github_com_burntsushi_toml", "github_com_pelletier_go_toml_v2")
CONTROL = "controls/toml/service-config.toml"
DIFFERENTIAL = "controls/toml/typed-scalars.toml"
REPEATS = 3
REPORT = ROOT / "data/go/toml/afl-feedback.json"
SANDBOX = ["--network", "none", "--read-only", "--cap-drop", "ALL",
           "--security-opt", "no-new-privileges", "--user", f"{os.getuid()}:{os.getgid()}"]


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])
    return result.stdout


def probe(manifest: dict, image: str, case: Path, work: Path, name: str) -> tuple[frozenset, frozenset]:
    common = ["docker", "run", "--rm", "--platform", manifest["platform"], *SANDBOX,
              "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
              "-v", f"{case}:/input/case:ro", "-v", f"{work}:/coverage"]
    run([*common, "--entrypoint", "/bin/sh", image,
         "/work/afl_trace", "/input/case", f"/coverage/{name}.features"])
    run([*common, "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap",
         image, "-m", "none", "-t", "10000", "-o", f"/coverage/{name}.map",
         "--", "/work/afl_proxy", "/input/case"])
    features = frozenset((work / f"{name}.features").read_text().splitlines()) - {""}
    tuples = frozenset((work / f"{name}.map").read_text().splitlines()) - {""}
    return features, tuples


def lines_per_file(features: frozenset, prefix: str) -> dict[str, int]:
    """Expand Go cover blocks (file:l1.c1,l2.c2) into executed parser source lines per file."""
    lines: dict[str, set[int]] = defaultdict(set)
    for feature in features:
        location, span = feature.rsplit(":", 1)
        start, end = span.split(",")
        first, last = int(start.split(".")[0]), int(end.split(".")[0])
        if end.split(".")[1] == "1" and last > first:
            last -= 1  # Go cover block end positions are exclusive.
        lines[location.removeprefix(prefix)].update(range(first, last + 1))
    return {name: len(lines[name]) for name in sorted(lines)}


def check(slug: str) -> dict:
    relative = Path("toml/go") / slug
    project, manifest = project_for("toml", "go", slug)
    if (manifest["control"], manifest["differential_control"]) != (CONTROL, DIFFERENTIAL):
        raise ValueError(f"{relative}: unexpected controls")
    for path, digest in ((CONTROL, manifest["control_sha256"]),
                         (DIFFERENTIAL, manifest["differential_control_sha256"])):
        if sha256((ROOT / path).read_bytes()).hexdigest() != digest:
            raise ValueError(f"{relative}: {path} hash differs from manifest")
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    if receipt["base_project_receipt_sha256"] != sha256((project / "verification.json").read_bytes()).hexdigest():
        raise RuntimeError(f"{relative}: overlay receipt is older than the project receipt")
    prefix = manifest["coverage_subject_prefix"]
    if f"ENV PARSARIUM_SUBJECT_PREFIX={prefix}" not in (overlay / "Dockerfile").read_text():
        raise RuntimeError(f"{relative}: overlay feedback is not scoped to the parser module")
    # The second control must produce its own expected typed tree in the base harness.
    output = run(["docker", "run", "--rm", "--platform", manifest["platform"], *SANDBOX,
                  "--tmpfs", "/tmp:rw,nosuid,size=64m",
                  "-v", f"{ROOT / DIFFERENTIAL}:/input/differential:ro",
                  "--entrypoint", "/work/harness.test", f"parsarium/toml-go-{slug}:local",
                  "-test.run=^TestDifferential$", "-test.v"])
    observed = next(line.removeprefix("OBSERVED_JSON:") for line in output.splitlines()
                    if line.startswith("OBSERVED_JSON:"))
    if json.loads(observed) != manifest["differential_expected_output"]:
        raise RuntimeError(f"{relative}: second control typed tree differs")
    image = receipt["image_id"]
    with tempfile.TemporaryDirectory(prefix="parsarium-toml-go-") as temporary:
        work = Path(temporary)
        controls = [probe(manifest, image, ROOT / CONTROL, work, f"control-{index}")
                    for index in range(REPEATS)]
        others = [probe(manifest, image, ROOT / DIFFERENTIAL, work, f"differential-{index}")
                  for index in range(REPEATS)]
    if len(set(controls)) != 1 or len(set(others)) != 1:
        raise RuntimeError(f"{relative}: repeated probes changed parser features or AFL++ map")
    first, other = controls[0], others[0]
    if len(first[0]) != receipt["parser_source_features"] or len(first[1]) != receipt["feedback_edges"]:
        raise RuntimeError(f"{relative}: control probe differs from overlay receipt")
    control_ids = {item.split(":", 1)[0] for item in first[1]}
    other_ids = {item.split(":", 1)[0] for item in other[1]}
    feature_difference = len(first[0] ^ other[0])
    tuple_difference = len(control_ids ^ other_ids)
    if feature_difference < 2 or tuple_difference < 2:
        raise RuntimeError(f"{relative}: second control did not change parser feedback")
    control_lines = lines_per_file(first[0], prefix)
    other_lines = lines_per_file(other[0], prefix)
    print(f"{relative}: {REPEATS} identical repeats per control; {feature_difference} parser blocks, "
          f"{tuple_difference} AFL++ tuples differ", flush=True)
    return {"project": str(relative), "pass": True,
            "feedback_kind": receipt["feedback_kind"],
            "feedback_scope": f"Go cover blocks under {prefix} only (harness and Go runtime excluded)",
            "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
            "base_project_receipt_sha256": receipt["base_project_receipt_sha256"],
            "control": CONTROL, "control_sha256": manifest["control_sha256"],
            "differential": DIFFERENTIAL,
            "differential_sha256": manifest["differential_control_sha256"],
            "differential_control_pass": True,
            "repeats_per_control": REPEATS,
            "repeated_control_identical": True,
            "repeated_differential_identical": True,
            "control_parser_features": len(first[0]),
            "control_afl_tuples": len(first[1]),
            "differential_parser_features": len(other[0]),
            "differential_afl_tuples": len(other[1]),
            "parser_feature_difference": feature_difference,
            "afl_tuple_difference": tuple_difference,
            "afl_tuples_only_control": len(control_ids - other_ids),
            "afl_tuples_only_differential": len(other_ids - control_ids),
            "control_parser_source_lines": sum(control_lines.values()),
            "differential_parser_source_lines": sum(other_lines.values()),
            "control_parser_lines_per_file": control_lines,
            "differential_parser_lines_per_file": other_lines}


def main() -> None:
    slugs = sys.argv[1:] or list(PROJECTS)
    if not set(slugs) <= set(PROJECTS):
        raise SystemExit(f"unknown Go TOML project: {sorted(set(slugs) - set(PROJECTS))}")
    fresh = {f"toml/go/{slug}": check(slug) for slug in slugs}
    kept = json.loads(REPORT.read_text())["results"] if REPORT.is_file() else []
    rows = {item["project"]: item for item in kept} | fresh
    results = [rows[f"toml/go/{slug}"] for slug in PROJECTS if f"toml/go/{slug}" in rows]
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "projects_total": len(results), "projects_passed": len(results),
        "differential_kind": "fixed_valid_typed_scalars",
        "results": results}, indent=2) + "\n")


if __name__ == "__main__":
    main()
