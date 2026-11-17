"""Recheck mp3-parser's two valid controls and parser-only AFL++ feedback."""

import json
from pathlib import Path
import sys

from verify_javascript_mp3_feedback import check


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data/javascript/mp3/mp3_parser-feedback-differential.json"


def main() -> None:
    if len(sys.argv) != 2 or sys.argv[1] not in {"--write", "--check"}:
        raise SystemExit("usage: verify_javascript_mp3_mp3_parser.py --write|--check")
    manifest = json.loads((ROOT / "projects/mp3/javascript/mp3_parser/manifest.json").read_text())
    source = "/work/node_modules/mp3-parser/lib/lib.js"
    if manifest["afl_coverage_subject_prefix"] != source:
        raise RuntimeError("AFL subject is not the MPEG frame reader source")
    result = check("mp3_parser")
    for key in ("control_only_features_by_file", "differential_only_features_by_file",
                "control_features_by_file"):
        values = result[key]
        if set(values) - {""}:
            raise RuntimeError(f"unexpected source file in parser feedback: {values}")
        result[key] = {"lib/lib.js": values.get("", 0)}
    result["parser_source_path"] = source
    result["release_tarball_sha256"] = manifest["source_sha256"]
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if sys.argv[1] == "--write":
        REPORT.write_text(output)
    elif REPORT.read_text() != output:
        raise SystemExit("mp3-parser feedback receipt changed")
    print(f"verified mp3-parser: {result['parser_feature_difference']} parser ranges, "
          f"{result['afl_tuple_difference']} AFL++ tuples differ")


if __name__ == "__main__":
    main()
