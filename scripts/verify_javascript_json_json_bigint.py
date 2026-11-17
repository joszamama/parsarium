"""Recheck json-bigint's two valid controls and parser-only AFL++ feedback."""

import json
from pathlib import Path
import sys

from verify_javascript_json_feedback import verify_project


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data/javascript/json/json-bigint-feedback-differential.json"


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"--write", "--check"}:
        raise SystemExit("usage: verify_javascript_json_json_bigint.py --write|--check")
    manifest = json.loads((ROOT / "projects/json/javascript/json_bigint/manifest.json").read_text())
    source = manifest["afl_coverage_subject_prefix"]
    if source != "/work/node_modules/json-bigint/lib/parse.js":
        raise RuntimeError("AFL subject is not the json-bigint parser source file")
    result = verify_project("json_bigint")
    # The shared verifier represents the exact-file prefix by an empty suffix.
    for key in ("control_only_features_by_file", "differential_only_features_by_file"):
        values = result[key]
        if set(values) - {""}:
            raise RuntimeError(f"unexpected parser source file: {values}")
        result[key] = {"lib/parse.js": values.get("", 0)}
    result["parser_source_path"] = source
    result["release_tarball_sha256"] = manifest["source_sha256"]
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if sys.argv[1] == "--write":
        REPORT.write_text(output)
    elif REPORT.read_text() != output:
        raise SystemExit("json-bigint feedback receipt changed")
    print(f"verified json-bigint: {result['parser_feature_difference']} parser ranges, "
          f"{result['afl_tuple_difference']} AFL++ tuples differ")


if __name__ == "__main__":
    main()
