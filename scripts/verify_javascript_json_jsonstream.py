"""Check the JSONStream AFL++ bridge: both valid controls replay to their pinned outputs,
repeated probes match, and the second control changes feedback. The bridge traces every
loaded package under /work/node_modules/, so the differential is split by package to keep
JSONStream's own index.js apart from the jsonparse tokenizer it delegates to."""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import tempfile

from run_case import ROOT, project_for
from verify_javascript_json_feedback import probe, run, sandbox


RELATIVE = Path("json/javascript/jsonstream")
REPORT = ROOT / "data/javascript/json/jsonstream-afl-feedback.json"
PACKAGES = ("JSONStream", "jsonparse", "through")
NODE_MODULES = "/work/node_modules/"


def package_of(feature: str) -> str:
    if not feature.startswith(NODE_MODULES):
        raise RuntimeError(f"feature outside node_modules: {feature}")
    name = feature[len(NODE_MODULES):].split("/", 1)[0]
    if name not in PACKAGES:
        raise RuntimeError(f"feature outside JSONStream, jsonparse and through: {feature}")
    return name


def by_package(features: set) -> dict:
    return {name: sum(package_of(item) == name for item in features) for name in PACKAGES}


def by_file(features: set) -> dict:
    files = {}
    for item in features:
        name = item[len(NODE_MODULES):].rsplit(":", 1)[0]
        files[name] = files.get(name, 0) + 1
    return dict(sorted(files.items()))


def main() -> None:
    project, manifest = project_for(*RELATIVE.parts)
    overlay = ROOT / "fuzzing/afl-native" / RELATIVE
    receipt = json.loads((overlay / "verification.json").read_text())
    base = json.loads((project / "verification.json").read_text())
    if receipt["base_image_id"] != base["image_id"]:
        raise ValueError("overlay was built from a different project image")
    if base["parser_source_lines_covered"] <= 0 or base["underlying_source_lines_covered"] <= 0:
        raise ValueError("project receipt lacks JSONStream or jsonparse source coverage")
    control, differential = ROOT / manifest["control"], ROOT / manifest["differential_control"]
    for path, digest in ((control, manifest["control_sha256"]),
                         (differential, manifest["differential_control_sha256"])):
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise ValueError(f"control hash mismatch: {path}")
    with tempfile.TemporaryDirectory(prefix="parsarium-jsonstream-") as temporary:
        work = Path(temporary)
        outputs = {}
        for name, path, expected in (("control", control, manifest["expected_output"]),
                                     ("differential", differential,
                                      manifest["differential_expected_output"])):
            outputs[name] = json.loads(run([*sandbox(manifest, path, work), "--entrypoint", "node",
                                            base["image_id"], "/work/replay.js", "/input/case"]))
            if outputs[name] != expected:
                raise RuntimeError(f"{name} output differs: {outputs[name]}")
        first = probe(manifest, receipt["image_id"], control, work, "first")
        repeat = probe(manifest, receipt["image_id"], control, work, "repeat")
        other = probe(manifest, receipt["image_id"], differential, work, "other")
        other_repeat = probe(manifest, receipt["image_id"], differential, work, "other-repeat")
    if first != repeat or other != other_repeat:
        raise RuntimeError("repeated probe changed parser features or AFL++ map")
    if len(first[0]) != receipt["parser_source_features"] or len(first[1]) != receipt["feedback_edges"]:
        raise RuntimeError("control probe differs from overlay receipt")
    feature_difference = len(first[0] ^ other[0])
    tuple_difference = len(first[1] ^ other[1])
    if not feature_difference or not tuple_difference:
        raise RuntimeError("second control did not change bridge feedback")
    changed = by_package(first[0] ^ other[0])
    if not changed["jsonparse"]:
        raise RuntimeError("second control did not change jsonparse feedback")
    result = {
        "schema_version": 1,
        "checked_at_utc": datetime.now(timezone.utc).isoformat(),
        "project": str(RELATIVE), "pass": True,
        "feedback_kind": receipt["feedback_kind"],
        "feedback_scope": "V8 source ranges in /work/node_modules/: JSONStream, jsonparse and through; "
                          "AFL++ tuples are not split by package",
        "overlay_receipt_sha256": sha256((overlay / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": base["image_id"], "overlay_image_id": receipt["image_id"],
        "control": manifest["control"], "control_sha256": manifest["control_sha256"],
        "control_output": outputs["control"],
        "differential": manifest["differential_control"],
        "differential_sha256": manifest["differential_control_sha256"],
        "differential_output": outputs["differential"],
        "repeated_control_identical": True, "repeated_differential_identical": True,
        "control_parser_features": len(first[0]), "control_afl_tuples": len(first[1]),
        "differential_parser_features": len(other[0]), "differential_afl_tuples": len(other[1]),
        "parser_feature_difference": feature_difference, "afl_tuple_difference": tuple_difference,
        "control_features_by_package": by_package(first[0]),
        "differential_features_by_package": by_package(other[0]),
        "feature_difference_by_package": changed,
        "package_only_feedback_differs": changed["JSONStream"] > 0,
        "control_only_features_by_file": by_file(first[0] - other[0]),
        "differential_only_features_by_file": by_file(other[0] - first[0]),
    }
    REPORT.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(f"{RELATIVE}: stable repeats; {feature_difference} features, {tuple_difference} AFL++ tuples "
          f"differ; by package {changed}", flush=True)


if __name__ == "__main__":
    main()
