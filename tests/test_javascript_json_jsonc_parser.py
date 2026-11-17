"""jsonc-parser's selected scope matches independent valid-control JSON trees."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/javascript/json"
PROJECT = ROOT / "projects/json/javascript/jsonc_parser"


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def unique_members(pairs: list) -> dict:
    if len({key for key, _ in pairs}) != len(pairs):
        raise ValueError("duplicate key in control")
    return dict(pairs)


def type_tag(value: object) -> dict:
    if value is None:
        return {"type": "null"}
    if isinstance(value, bool):
        return {"type": "boolean", "value": value}
    if isinstance(value, (int, float)):
        if isinstance(value, int) and abs(value) > (1 << 53) - 1:
            raise ValueError("control number outside exact JS Number range")
        return {"type": "number", "value": value}
    if isinstance(value, str):
        return {"type": "string", "value": value}
    if isinstance(value, list):
        return {"type": "array", "items": [type_tag(item) for item in value]}
    return {"type": "object", "members": {
        key: type_tag(value[key]) for key in sorted(value)
    }}


class JavaScriptJsoncParserTest(unittest.TestCase):
    def test_both_type_tagged_trees_match_python_json_oracle(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        for control_key, hash_key, output_key in (
                ("control", "control_sha256", "expected_output"),
                ("differential_control", "differential_control_sha256",
                 "differential_expected_output")):
            data = (ROOT / manifest[control_key]).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), manifest[hash_key])
            oracle = json.loads(data.decode("utf-8"), object_pairs_hook=unique_members)
            self.assertEqual(type_tag(oracle), manifest[output_key])

    def test_release_and_parser_scoped_feedback_are_pinned(self):
        parser, = [item for item in read(BASE / "parsers.json")
                   if item["name"] == "jsonc-parser"]
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")["jsonc-parser"]
        npm_lock = read(PROJECT / "package-lock.json")["packages"]["node_modules/jsonc-parser"]
        self.assertEqual((parser["version"], parser["npm_integrity"], parser["tarball_sha256"]),
                         (lock["release"], lock["npm_integrity"], lock["source_sha256"]))
        self.assertEqual((npm_lock["version"], npm_lock["integrity"]),
                         (lock["release"], lock["npm_integrity"]))
        self.assertEqual(parser["popularity"]["value"],
                         read(BASE / "registry-snapshot.json")["downloads"]["jsonc-parser"]["value"])
        self.assertEqual(read(PROJECT / "verification.json")["parser_source_files"], 2)
        self.assertEqual(read(PROJECT / "verification.json")["parser_source_lines_covered"], 617)
        source = "/work/node_modules/jsonc-parser/lib/umd/impl/scanner.js"
        self.assertEqual(manifest["coverage_subject_prefix"], "/work/node_modules/jsonc-parser/lib/umd/impl/")
        self.assertEqual(manifest["afl_coverage_subject_prefix"], source)
        overlay = ROOT / "fuzzing/afl-native/json/javascript/jsonc_parser"
        self.assertIn(f"ENV PARSARIUM_SUBJECT_PREFIX={source}",
                      (overlay / "Dockerfile").read_text())
        feedback = read(BASE / "jsonc-parser-feedback-differential.json")
        self.assertEqual(feedback["overlay_receipt_sha256"],
                         sha256((overlay / "verification.json").read_bytes()).hexdigest())
        self.assertTrue(feedback["repeated_control_identical"])
        self.assertTrue(feedback["repeated_differential_identical"])
        self.assertGreater(feedback["parser_feature_difference"], 0)
        self.assertGreater(feedback["afl_tuple_difference"], 0)
        self.assertEqual(set(feedback["control_only_features_by_file"]), {"lib/umd/impl/scanner.js"})
        self.assertEqual(set(feedback["differential_only_features_by_file"]), {"lib/umd/impl/scanner.js"})

    def test_documented_tree_api_uses_strict_json_options_and_checks_errors(self):
        adapter = (PROJECT / "adapter.mjs").read_text(encoding="utf-8")
        self.assertIn("const { parseTree } = require('jsonc-parser')", adapter)
        self.assertIn("disallowComments: true", adapter)
        self.assertIn("allowTrailingComma: false", adapter)
        self.assertIn("allowEmptyContent: false", adapter)
        self.assertIn("errors.length !== 0", adapter)
        self.assertNotIn("JSON.parse(", adapter)


if __name__ == "__main__":
    unittest.main()
