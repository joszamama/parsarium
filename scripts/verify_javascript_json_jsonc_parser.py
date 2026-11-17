"""Recheck jsonc-parser's two valid controls and parser-only AFL++ feedback."""

import json
from pathlib import Path
import sys

from verify_javascript_json_feedback import verify_project


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data/javascript/json/jsonc-parser-feedback-differential.json"


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"--write", "--check"}:
        raise SystemExit("usage: verify_javascript_json_jsonc_parser.py --write|--check")
    manifest = json.loads((ROOT / "projects/json/javascript/jsonc_parser/manifest.json").read_text())
    source = manifest["afl_coverage_subject_prefix"]
    if source != "/work/node_modules/jsonc-parser/lib/umd/impl/scanner.js":
        raise RuntimeError("AFL subject is not the jsonc-parser scanner source file")
    result = verify_project("jsonc_parser")
    # The shared verifier reports files relative to the V8 source directory.
    for key in ("control_only_features_by_file", "differential_only_features_by_file"):
        values = result[key]
        if set(values) - {"scanner.js"}:
            raise RuntimeError(f"unexpected parser source file: {values}")
        result[key] = {"lib/umd/impl/scanner.js": values.get("scanner.js", 0)}
    result["parser_source_path"] = source
    result["release_tarball_sha256"] = manifest["source_sha256"]
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if sys.argv[1] == "--write":
        REPORT.write_text(output)
    elif REPORT.read_text() != output:
        raise SystemExit("jsonc-parser feedback receipt changed")
    print(f"verified jsonc-parser: {result['parser_feature_difference']} parser ranges, "
          f"{result['afl_tuple_difference']} AFL++ tuples differ")


if __name__ == "__main__":
    main()
