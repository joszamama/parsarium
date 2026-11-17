"""Recheck one PHP TOML path's two valid controls, parser source lines and AFL++ feedback.

usage: verify_php_toml_feedback.py SLUG --write|--check

The Xdebug control runner must reproduce both hand-written typed trees; the parser-line
AFL++ bridge must repeat identically (three runs) on each control and differ between the two.
--write also refreshes this path's row in data/php/toml/afl-feedback.json.
"""

from collections import Counter
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import sys
import tempfile

from verify_php_json_feedback import probe
from verify_php_json_line_feedback import replay


ROOT = Path(__file__).resolve().parents[1]
REPEATS = 3
REPORTS = {
    "internal_toml": "internal-toml-feedback-differential.json",
    "php_collective_toml": "php-collective-toml-feedback-differential.json",
    "petalbranch_toml": "petalbranch-toml-feedback-differential.json",
}
CELL_REPORT = ROOT / "data/php/toml/afl-feedback.json"


def main() -> None:
    if len(sys.argv) != 3 or sys.argv[1] not in REPORTS or sys.argv[2] not in {"--write", "--check"}:
        raise SystemExit(f"usage: verify_php_toml_feedback.py {'|'.join(REPORTS)} --write|--check")
    slug, mode = sys.argv[1], sys.argv[2]
    project = ROOT / "projects/toml/php" / slug
    overlay_dir = ROOT / "fuzzing/afl-native/toml/php" / slug
    report = ROOT / "data/php/toml" / REPORTS[slug]
    manifest = json.loads((project / "manifest.json").read_text())
    base = json.loads((project / "verification.json").read_text())
    overlay = json.loads((overlay_dir / "verification.json").read_text())
    prefix = manifest["coverage_subject_prefix"]
    if f"ENV PARSARIUM_SUBJECT_PREFIX={prefix}\n" not in (overlay_dir / "Dockerfile").read_text():
        raise RuntimeError("AFL++ bridge is not scoped to the package source")
    if overlay["base_image_id"] != base["image_id"]:
        raise RuntimeError("AFL++ overlay was not built from the verified project image")
    if overlay["base_project_receipt_sha256"] != sha256((project / "verification.json").read_bytes()).hexdigest():
        raise RuntimeError("AFL++ overlay receipt predates the project receipt")
    control = ROOT / manifest["control"]
    differential = ROOT / manifest["differential_control"]
    for path, digest in ((control, manifest["control_sha256"]),
                         (differential, manifest["differential_control_sha256"])):
        if sha256(path.read_bytes()).hexdigest() != digest:
            raise RuntimeError(f"{path.name}: control bytes changed")
    with tempfile.TemporaryDirectory(prefix=f"parsarium-toml-{slug}-") as temporary:
        work = Path(temporary)
        lines = replay(manifest, base["image_id"], control, work / "control-lines", prefix)
        other_lines = replay(manifest, base["image_id"], differential, work / "differential-lines", prefix)
        image = overlay["image_id"]
        firsts = [probe(manifest, image, control, work, f"control-{index}", True) for index in range(REPEATS)]
        others = [probe(manifest, image, differential, work, f"differential-{index}", True)
                  for index in range(REPEATS)]
    if lines["output"] != manifest["expected_output"]:
        raise RuntimeError("service-config typed tree differs from manifest")
    if other_lines["output"] != manifest["differential_expected_output"]:
        raise RuntimeError("typed-scalars typed tree differs from manifest")
    if any(item != firsts[0] for item in firsts) or any(item != others[0] for item in others):
        raise RuntimeError("repeated probe changed parser features or AFL++ map")
    first, other = firsts[0], others[0]
    if len(first[0]) != overlay["parser_source_features"] or len(first[1]) != overlay["feedback_edges"]:
        raise RuntimeError("control probe differs from overlay receipt")
    if len(first[0]) != lines["parser_source_lines_covered"]:
        raise RuntimeError("AFL++ bridge features differ from Xdebug control lines")
    if len(other[0]) != other_lines["parser_source_lines_covered"]:
        raise RuntimeError("AFL++ bridge features differ from Xdebug differential lines")
    feature_difference = len(first[0] ^ other[0])
    tuple_difference = len({item.split(":", 1)[0] for item in first[1]} ^
                           {item.split(":", 1)[0] for item in other[1]})
    if feature_difference < 2 or tuple_difference < 2:
        raise RuntimeError("differential control did not change parser feedback")

    def by_file(features: set) -> dict:
        return dict(sorted(Counter(item.removeprefix(prefix).rsplit(":", 1)[0]
                                   for item in features).items()))

    result = {
        "project": f"toml/php/{slug}", "pass": True,
        "feedback_kind": overlay["feedback_kind"],
        "overlay_receipt_sha256": sha256((overlay_dir / "verification.json").read_bytes()).hexdigest(),
        "base_project_receipt_sha256": overlay["base_project_receipt_sha256"],
        "base_image_id": base["image_id"], "overlay_image_id": image,
        "release_source_sha256": manifest["source_sha256"],
        "parser_source_prefix": prefix,
        "control": manifest["control"], "control_sha256": manifest["control_sha256"],
        "differential": manifest["differential_control"],
        "differential_sha256": manifest["differential_control_sha256"],
        "control_output_matches_oracle": True, "differential_output_matches_oracle": True,
        "typed_tree_keys_sorted": True,
        "repeats_per_control": REPEATS,
        "control_source_lines_by_file": lines["lines_by_file"],
        "differential_source_lines_by_file": other_lines["lines_by_file"],
        "control_parser_source_lines": lines["parser_source_lines_covered"],
        "differential_parser_source_lines": other_lines["parser_source_lines_covered"],
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
        cell = (json.loads(CELL_REPORT.read_text()) if CELL_REPORT.is_file()
                else {"schema_version": 1, "results": []})
        rows = [row for row in cell["results"] if row["project"] != result["project"]]
        rows.append({key: result[key] for key in (
            "project", "pass", "feedback_kind", "overlay_receipt_sha256", "control", "control_sha256",
            "differential", "differential_sha256", "repeats_per_control", "repeated_control_identical",
            "repeated_differential_identical", "control_parser_features", "control_afl_tuples",
            "differential_parser_features", "differential_afl_tuples", "parser_feature_difference",
            "afl_tuple_difference")})
        rows.sort(key=lambda row: row["project"])
        CELL_REPORT.write_text(json.dumps({
            "schema_version": 1,
            "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "projects_total": len(rows), "projects_passed": len(rows),
            "differential_kind": "fixed_valid_typed_scalars",
            "results": rows}, indent=2) + "\n")
    elif report.read_text() != output:
        raise SystemExit(f"{slug} feedback receipt changed")
    print(f"verified {slug}: {feature_difference} parser lines, {tuple_difference} AFL++ tuples differ")


if __name__ == "__main__":
    main()
