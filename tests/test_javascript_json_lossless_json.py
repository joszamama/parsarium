"""Check lossless-json control receipts against a numeric-lexeme JSON oracle."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/json/javascript/lossless_json"
MANIFEST = json.loads((PROJECT / "manifest.json").read_text())
spec = importlib.util.spec_from_file_location("lossless_json_oracle", PROJECT / "oracle.py")
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)


class LosslessJSONEvidenceTest(unittest.TestCase):
    def test_both_control_trees_and_numeric_lexemes(self):
        for path_key, digest_key, output_key in (
            ("control", "control_sha256", "expected_output"),
            ("differential_control", "differential_control_sha256",
             "differential_expected_output"),
        ):
            data = (ROOT / MANIFEST[path_key]).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), MANIFEST[digest_key])
            self.assertEqual(oracle.summarize(data), MANIFEST[output_key])
        self.assertEqual(MANIFEST["expected_output"]["members"]["ratio"],
                         {"type": "LosslessNumber", "raw": "-0.25e1"})
        self.assertEqual(MANIFEST["differential_expected_output"]["items"][1],
                         {"type": "LosslessNumber", "raw": "2.5e-1"})

    def test_feedback_is_parser_scoped_and_input_dependent(self):
        self.assertEqual(MANIFEST["afl_coverage_subject_prefix"],
                         "/work/node_modules/lossless-json/lib/esm/parse.js")
        receipt = json.loads((ROOT / "data/javascript/json/lossless-json-feedback.json").read_text())
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["repeats_per_control"], 3)
        self.assertEqual(receipt["parser_feature_difference"], 8)
        self.assertEqual(receipt["afl_tuple_difference"], 8)
        self.assertTrue(all(item.startswith(MANIFEST["afl_coverage_subject_prefix"])
                            for item in receipt["control_only_features"]
                            + receipt["differential_only_features"]))


if __name__ == "__main__":
    unittest.main()
