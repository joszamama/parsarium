"""Recheck one PHP YAML path's two valid controls, parser source lines and AFL++ feedback.

usage: verify_php_yaml_feedback.py SLUG --write|--check

The Xdebug control runner must reproduce both oracle trees from
controls/yaml/check_controls.py; the parser-line AFL++ bridge must repeat
identically three times on each control and differ between the two controls.
"""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import runpy
import sys
import tempfile

from verify_php_json_feedback import probe
from verify_php_json_line_feedback import replay


ROOT = Path(__file__).resolve().parents[1]
REPORTS = {
    "symfony_yaml": "symfony-yaml-feedback-differential.json",
    "purrphp_yaml": "purrphp-yaml-feedback-differential.json",
}
REPEATS = 3


def oracle_output(name: str) -> dict:
    checks = runpy.run_path(str(ROOT / "controls/yaml/check_controls.py"))
    tree = checks["EXPECTED"][name]
    return {**checks["summary"](tree), "tree": tree}


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] not in REPORTS or sys.argv[2] not in {"--write", "--check"}:
        raise SystemExit(f"usage: verify_php_yaml_feedback.py {'|'.join(REPORTS)} --write|--check")
    slug, mode = sys.argv[1], sys.argv[2]
    project = ROOT / "projects/yaml/php" / slug
    overlay_dir = ROOT / "fuzzing/afl-native/yaml/php" / slug
    report = ROOT / "data/php/yaml" / REPORTS[slug]
    manifest = json.loads((project / "manifest.json").read_text())
    base = json.loads((project / "verification.json").read_text())
    overlay = json.loads((overlay_dir / "verification.json").read_text())
    prefix = manifest["coverage_subject_prefix"]
    if f"ENV PARSARIUM_SUBJECT_PREFIX={prefix}\n" not in (overlay_dir / "Dockerfile").read_text():
        raise RuntimeError("AFL++ bridge is not scoped to the package source")
    if overlay["base_image_id"] != base["image_id"]:
        raise RuntimeError("AFL++ overlay was not built from the verified project image")
    control = ROOT / manifest["control"]
    differential = ROOT / manifest["differential_control"]
    for path, digest in ((control, manifest["control_sha256"]),
                         (differential, manifest["differential_control_sha256"])):
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError(f"{path.name}: control bytes changed")
    if manifest["expected_output"] != oracle_output(control.name):
        raise RuntimeError("manifest control tree differs from the YAML oracle")
    if manifest["differential_expected_output"] != oracle_output(differential.name):
        raise RuntimeError("manifest differential tree differs from the YAML oracle")
    with tempfile.TemporaryDirectory(prefix=f"parsarium-{slug}-") as temporary:
        work = Path(temporary)
        lines = replay(manifest, base["image_id"], control, work / "control-lines", prefix)
        other_lines = replay(manifest, base["image_id"], differential, work / "differential-lines", prefix)
        image = overlay["image_id"]
        firsts = [probe(manifest, image, control, work, f"control-{index}", True) for index in range(REPEATS)]
        others = [probe(manifest, image, differential, work, f"other-{index}", True) for index in range(REPEATS)]
    if lines["output"] != manifest["expected_output"]:
        raise RuntimeError("catalog.yaml tree differs from manifest")
    if other_lines["output"] != manifest["differential_expected_output"]:
        raise RuntimeError("order.yaml tree differs from manifest")
    if any(item != firsts[0] for item in firsts) or any(item != others[0] for item in others):
        raise RuntimeError("repeated probe changed parser features or AFL++ map")
    first, other = firsts[0], others[0]
    if len(first[0]) != overlay["parser_source_features"] or len(first[1]) != overlay["feedback_edges"]:
        raise RuntimeError("control probe differs from overlay receipt")
    if len(first[0]) != lines["parser_source_lines_covered"]:
        raise RuntimeError("AFL++ bridge features differ from Xdebug control lines")
    feature_difference = len(first[0] ^ other[0])
    tuple_difference = len({item.split(":", 1)[0] for item in first[1]} ^
                           {item.split(":", 1)[0] for item in other[1]})
    if not feature_difference or not tuple_difference:
        raise RuntimeError("differential control did not change parser feedback")

    def by_file(features: set) -> dict:
        return dict(sorted(Counter(item.removeprefix(prefix).rsplit(":", 1)[0]
                                   for item in features).items()))

    result = {
        "project": f"yaml/php/{slug}", "pass": True,
        "feedback_kind": overlay["feedback_kind"],
        "oracle": "controls/yaml/check_controls.py hand-written typed trees (cross-checked with Ruby Psych)",
        "overlay_receipt_sha256": sha256((overlay_dir / "verification.json").read_bytes()).hexdigest(),
        "base_image_id": base["image_id"], "overlay_image_id": image,
        "release_source_sha256": manifest["source_sha256"],
        "parser_source_prefix": prefix,
        "control": manifest["control"], "control_sha256": manifest["control_sha256"],
        "differential": manifest["differential_control"],
        "differential_sha256": manifest["differential_control_sha256"],
        "control_output_matches_oracle": True, "differential_output_matches_oracle": True,
        "ordered_members_and_scalar_types_checked": True,
        "control_source_lines_by_file": lines["lines_by_file"],
        "differential_source_lines_by_file": other_lines["lines_by_file"],
        "runs_per_control": REPEATS,
        "repeated_control_identical": True, "repeated_differential_identical": True,
        "control_parser_features": len(first[0]), "control_afl_tuples": len(first[1]),
        "differential_parser_features": len(other[0]), "differential_afl_tuples": len(other[1]),
        "parser_feature_difference": feature_difference,
        "afl_tuple_difference": tuple_difference,
        "control_only_features_by_file": by_file(first[0] - other[0]),
        "differential_only_features_by_file": by_file(other[0] - first[0]),
    }
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if mode == "--write":
        report.write_text(output)
    elif report.read_text() != output:
        raise SystemExit(f"{slug} feedback receipt changed")
    print(f"verified {slug}: {feature_difference} parser lines, {tuple_difference} AFL++ tuples differ")


if __name__ == "__main__":
    main()
