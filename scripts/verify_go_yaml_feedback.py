"""Check Go YAML AFL++ bridges: three repeats per valid control are identical and the controls differ.

Both controls are also replayed through the verified project image: TestControl
and TestDifferential compare the parsed typed trees with the hand-written oracle
of controls/yaml/check_controls.py. Writes data/go/yaml/afl-feedback.json.
"""

from datetime import datetime, timezone
from hashlib import sha256
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

from run_case import ROOT, project_for


PROJECTS = ("gopkg_in_yaml_v2", "gopkg_in_yaml_v3", "github_com_goccy_go_yaml",
            "go_yaml_in_yaml_v4", "github_com_go_rotini_yaml",
            "github_com_yongjohnlee80_golib_parse_yaml", "github_com_tabnas_yaml_go")
CONTROL = "controls/yaml/catalog.yaml"
DIFFERENTIAL = "controls/yaml/order.yaml"
REPORT = ROOT / "data/go/yaml/afl-feedback.json"
REPEATS = 3


def oracle() -> dict:
    spec = importlib.util.spec_from_file_location("yaml_controls", ROOT / "controls/yaml/check_controls.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.EXPECTED


def run(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, timeout=180)
    if result.returncode:
        raise RuntimeError((result.stdout + result.stderr)[-1000:])
    return result.stdout


def sandbox(manifest: dict, mounts: list[str]) -> list[str]:
    return ["docker", "run", "--rm", "--platform", manifest["platform"],
            "--network", "none", "--read-only", "--cap-drop", "ALL",
            "--security-opt", "no-new-privileges",
            "--user", f"{os.getuid()}:{os.getgid()}",
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m", *mounts]


def probe(manifest: dict, image: str, case: Path, work: Path, name: str) -> tuple[frozenset, frozenset]:
    common = sandbox(manifest, ["-v", f"{case}:/input/case:ro", "-v", f"{work}:/coverage"])
    run([*common, "--entrypoint", "/bin/sh", image,
         "/work/afl_trace", "/input/case", f"/coverage/{name}.features"])
    run([*common, "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap",
         image, "-m", "none", "-t", "10000", "-o", f"/coverage/{name}.map",
         "--", "/work/afl_proxy", "/input/case"])
    features = frozenset((work / f"{name}.features").read_text().splitlines()) - {""}
    tuples = frozenset((work / f"{name}.map").read_text().splitlines()) - {""}
    prefix = manifest["coverage_subject_prefix"]
    if not features or not tuples or any(not item.startswith(prefix) for item in features):
        raise RuntimeError("feedback is empty or outside the parser package")
    return features, tuples


def files(features: frozenset) -> dict:
    counts: dict[str, int] = {}
    for item in features:
        name = item.split(":", 1)[0].rsplit("/", 1)[-1]
        counts[name] = counts.get(name, 0) + 1
    return dict(sorted(counts.items()))


def check(slug: str, expected: dict) -> dict:
    relative = Path("yaml/go") / slug
    project, manifest = project_for("yaml", "go", slug)
    if manifest["control"] != CONTROL or manifest["differential_control"] != DIFFERENTIAL:
        raise ValueError(f"{relative}: unexpected controls")
    if (manifest["expected_output"] != {"tree": expected["catalog.yaml"]} or
            manifest["differential_expected_output"] != {"tree": expected["order.yaml"]}):
        raise ValueError(f"{relative}: manifest trees differ from the oracle")
    for path, digest in ((CONTROL, manifest["control_sha256"]),
                         (DIFFERENTIAL, manifest["differential_control_sha256"])):
        if sha256((ROOT / path).read_bytes()).hexdigest() != digest:
            raise ValueError(f"{relative}: control hash changed")
    overlay = ROOT / "fuzzing/afl-native" / relative
    receipt = json.loads((overlay / "verification.json").read_text())
    base = json.loads((project / "verification.json").read_text())
    if receipt["base_image_id"] != base["image_id"]:
        raise RuntimeError(f"{relative}: overlay base differs from the verified project image")
    run([*sandbox(manifest, ["-v", f"{ROOT / CONTROL}:/input/control:ro",
                             "-v", f"{ROOT / DIFFERENTIAL}:/input/differential:ro"]),
         "--entrypoint", "/work/harness.test", base["image_id"],
         "-test.run=^(TestControl|TestDifferential)$", "-test.v"])
    image = receipt["image_id"]
    with tempfile.TemporaryDirectory(prefix="parsarium-yaml-go-") as temporary:
        work = Path(temporary)
        firsts = [probe(manifest, image, ROOT / CONTROL, work, f"control-{i}") for i in range(REPEATS)]
        others = [probe(manifest, image, ROOT / DIFFERENTIAL, work, f"other-{i}") for i in range(REPEATS)]
    if any(item != firsts[0] for item in firsts) or any(item != others[0] for item in others):
        raise RuntimeError(f"{relative}: repeated probes changed parser features or AFL++ map")
    first, other = firsts[0], others[0]
    if len(first[0]) != receipt["parser_source_features"] or len(first[1]) != receipt["feedback_edges"]:
        raise RuntimeError(f"{relative}: control probe differs from overlay receipt")
    feature_difference = len(first[0] ^ other[0])
    tuple_difference = len({item.split(":", 1)[0] for item in first[1]} ^
                           {item.split(":", 1)[0] for item in other[1]})
    if not feature_difference or not tuple_difference:
        raise RuntimeError(f"{relative}: differential input did not change parser feedback")
    print(f"{relative}: {REPEATS} identical repeats per control; {feature_difference} parser blocks, "
          f"{tuple_difference} AFL++ tuples differ", flush=True)
    return {"project": str(relative), "pass": True,
            "feedback_kind": receipt["feedback_kind"],
            "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
            "control": CONTROL,
            "control_sha256": manifest["control_sha256"],
            "differential": DIFFERENTIAL,
            "differential_sha256": manifest["differential_control_sha256"],
            "oracle": "controls/yaml/check_controls.py EXPECTED typed trees (hand-written, Psych cross-checked)",
            "control_tree_pass": True, "differential_tree_pass": True,
            "runs_per_control": REPEATS,
            "repeated_control_identical": True, "repeated_differential_identical": True,
            "control_parser_features": len(first[0]),
            "control_afl_tuples": len(first[1]),
            "differential_parser_features": len(other[0]),
            "differential_afl_tuples": len(other[1]),
            "parser_feature_difference": feature_difference,
            "afl_tuple_difference": tuple_difference,
            "control_features_by_file": files(first[0]),
            "difference_features_by_file": files(first[0] ^ other[0])}


def main() -> None:
    slugs = sys.argv[1:] or list(PROJECTS)
    if not set(slugs) <= set(PROJECTS):
        raise SystemExit(f"unknown Go YAML project: {sorted(set(slugs) - set(PROJECTS))}")
    expected = oracle()
    fresh = {f"yaml/go/{slug}": check(slug, expected) for slug in slugs}
    kept = json.loads(REPORT.read_text())["results"] if REPORT.is_file() else []
    rows = {item["project"]: item for item in kept} | fresh
    results = [rows[f"yaml/go/{slug}"] for slug in PROJECTS if f"yaml/go/{slug}" in rows]
    REPORT.write_text(json.dumps({
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "projects_total": len(results), "projects_passed": len(results),
        "differential_kind": "fixed_valid_block_sequence_yaml",
        "results": results}, indent=2) + "\n")


if __name__ == "__main__":
    main()
