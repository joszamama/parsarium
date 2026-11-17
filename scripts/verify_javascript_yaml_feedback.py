"""Check a JavaScript YAML path on both valid controls and its parser-range AFL++ feedback.

For one project under projects/yaml/javascript/<slug>, both controls must replay to the
hand-written typed trees in controls/yaml/check_controls.py, each control is probed three
times through the AFL++ overlay (parser source ranges and afl-showmap tuples must repeat
exactly), and the two controls must differ in parser features and AFL++ tuples.

Usage: python3 scripts/verify_javascript_yaml_feedback.py SLUG --write|--check
"""

from datetime import datetime, timezone
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = runpy.run_path(str(ROOT / "controls/yaml/check_controls.py"))["EXPECTED"]
CONTROLS = {"controls/yaml/catalog.yaml": "catalog.yaml", "controls/yaml/order.yaml": "order.yaml"}
REPEATS = 3


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
            "--tmpfs", "/tmp:rw,exec,nosuid,size=64m",
            "-v", f"{case}:/input/case:ro", "-v", f"{work}:/coverage"]


def probe(manifest: dict, image: str, case: Path, work: Path, name: str) -> tuple[frozenset, frozenset]:
    common = sandbox(manifest, case, work)
    run([*common, "--entrypoint", "/bin/sh", image,
         "/work/afl_trace", "/input/case", f"/coverage/{name}.features"])
    run([*common, "-e", "AFL_MAP_SIZE=65536", "--entrypoint", "afl-showmap",
         image, "-m", "none", "-t", "30000", "-o", f"/coverage/{name}.map",
         "--", "/work/afl_proxy", "/input/case"])
    features = frozenset(set((work / f"{name}.features").read_text().splitlines()) - {""})
    tuples = frozenset(line.split(":", 1)[0] for line in (work / f"{name}.map").read_text().splitlines() if line)
    return features, tuples


def verify(slug: str) -> dict:
    project = ROOT / "projects/yaml/javascript" / slug
    overlay = ROOT / "fuzzing/afl-native/yaml/javascript" / slug
    manifest = json.loads((project / "manifest.json").read_text())
    base = json.loads((project / "verification.json").read_text())
    receipt = json.loads((overlay / "verification.json").read_text())
    if receipt["base_image_id"] != base["image_id"]:
        raise RuntimeError("overlay was built from a different project image")
    if receipt["base_project_receipt_sha256"] != sha256((project / "verification.json").read_bytes()).hexdigest():
        raise RuntimeError("overlay was built from a different project receipt")
    control, differential = ROOT / manifest["control"], ROOT / manifest["differential_control"]
    for path, digest in ((control, manifest["control_sha256"]),
                         (differential, manifest["differential_control_sha256"])):
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError(f"control hash mismatch: {path}")
    for key, path in (("expected_output", manifest["control"]),
                      ("differential_expected_output", manifest["differential_control"])):
        if manifest[key] != {"tree": EXPECTED[CONTROLS[path]]}:
            raise RuntimeError(f"{key} differs from the hand-written YAML oracle")
    prefix = manifest["afl_coverage_subject_prefix"]
    with tempfile.TemporaryDirectory(prefix="parsarium-yaml-js-") as temporary:
        work = Path(temporary)
        outputs = {}
        for name, case in (("control", control), ("differential", differential)):
            outputs[name] = json.loads(run([*sandbox(manifest, case, work), "--entrypoint", "node",
                                            base["image_id"], "/work/replay.js", "/input/case"]))
        if outputs["control"] != manifest["expected_output"]:
            raise RuntimeError("primary control output differs")
        if outputs["differential"] != manifest["differential_expected_output"]:
            raise RuntimeError("second control output differs")
        firsts = [probe(manifest, receipt["image_id"], control, work, f"control-{i}") for i in range(REPEATS)]
        others = [probe(manifest, receipt["image_id"], differential, work, f"other-{i}") for i in range(REPEATS)]
    if len(set(firsts)) != 1 or len(set(others)) != 1:
        raise RuntimeError("repeated probes changed parser features or AFL++ map")
    first, other = firsts[0], others[0]
    if any(not feature.startswith(prefix) for feature in first[0] | other[0]):
        raise RuntimeError("feedback outside the parser package source")
    if len(first[0]) != receipt["parser_source_features"] or len(first[1]) != receipt["feedback_edges"]:
        raise RuntimeError("control probe differs from overlay receipt")
    feature_difference = len(first[0] ^ other[0])
    tuple_difference = len(first[1] ^ other[1])
    if not feature_difference or not tuple_difference:
        raise RuntimeError("second control did not change parser feedback")

    def by_file(items) -> dict:
        root = prefix if prefix.endswith("/") else prefix.rsplit("/", 1)[0] + "/"
        counts: dict[str, int] = {}
        for item in items:
            name = item[len(root):].rsplit(":", 1)[0]
            counts[name] = counts.get(name, 0) + 1
        return dict(sorted(counts.items()))

    return {"checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "project": f"yaml/javascript/{slug}", "pass": True,
            "input_kind": "two fixed valid schema-neutral YAML 1.2 controls",
            "oracle": "hand-written typed trees in controls/yaml/check_controls.py (cross-checked there with Ruby Psych/libyaml)",
            "feedback_kind": receipt["feedback_kind"],
            "feedback_scope": f"V8 source ranges under {prefix}, mapped to the AFL++ bitmap by the Parsarium JavaScript bridge",
            "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
            "base_image_id": base["image_id"], "overlay_image_id": receipt["image_id"],
            "control": manifest["control"], "control_sha256": manifest["control_sha256"],
            "differential": manifest["differential_control"],
            "differential_sha256": manifest["differential_control_sha256"],
            "control_matches_oracle": True, "differential_matches_oracle": True,
            "runs_per_control": REPEATS,
            "repeated_control_identical": True, "repeated_differential_identical": True,
            "control_parser_features": len(first[0]), "control_afl_tuples": len(first[1]),
            "differential_parser_features": len(other[0]), "differential_afl_tuples": len(other[1]),
            "parser_feature_difference": feature_difference, "afl_tuple_difference": tuple_difference,
            "control_only_features_by_file": by_file(first[0] - other[0]),
            "differential_only_features_by_file": by_file(other[0] - first[0])}


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[2] not in {"--write", "--check"}:
        raise SystemExit("usage: verify_javascript_yaml_feedback.py SLUG --write|--check")
    slug = sys.argv[1]
    manifest = json.loads((ROOT / "projects/yaml/javascript" / slug / "manifest.json").read_text())
    report = ROOT / "data/javascript/yaml" / f"{manifest['package']}-valid-feedback.json"
    result = verify(slug)
    if sys.argv[2] == "--write":
        report.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    else:
        pinned = json.loads(report.read_text())
        volatile = {"checked_at_utc"}
        if {k: v for k, v in pinned.items() if k not in volatile} != \
                {k: v for k, v in result.items() if k not in volatile}:
            raise SystemExit(f"{slug} feedback receipt changed")
    print(f"verified {slug}: {result['parser_feature_difference']} parser ranges, "
          f"{result['afl_tuple_difference']} AFL++ tuples differ")


if __name__ == "__main__":
    main()
