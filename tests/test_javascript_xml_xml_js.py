"""Pin the xml-js API path, its independent controls, and parser-scoped feedback."""

from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "controls/xml"))
from check_controls import summarize  # noqa: E402


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


class XmlJsPathTest(unittest.TestCase):
    def setUp(self):
        self.project = ROOT / "projects/xml/javascript/xml_js"
        self.manifest = read(self.project / "manifest.json")
        self.receipt = read(self.project / "verification.json")
        self.parser, = (entry for entry in read(ROOT / "data/javascript/xml/parsers.json")
                        if entry["name"] == "xml-js")

    def test_both_controls_match_independent_namespace_oracle(self):
        for control_key, hash_key, output_key in (
            ("control", "control_sha256", "expected_output"),
            ("differential_control", "differential_control_sha256", "differential_expected_output"),
        ):
            data = (ROOT / self.manifest[control_key]).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), self.manifest[hash_key])
            self.assertEqual(self.manifest[output_key], summarize(data))
        self.assertEqual(self.receipt["output"], self.manifest["expected_output"])
        self.assertTrue(self.receipt["pass"])

    def test_pinned_sources_and_shared_family(self):
        lock = read(self.project / "source-lock.json")["xml-js"]
        packages = read(self.project / "package-lock.json")["packages"]
        sax, = (entry for entry in read(ROOT / "data/javascript/xml/parsers.json")
                if entry["name"] == "sax")
        self.assertEqual(lock["source_sha256"], self.parser["tarball_sha256"])
        self.assertEqual(lock["npm_integrity"], packages["node_modules/xml-js"]["integrity"])
        self.assertEqual(packages["node_modules/sax"]["integrity"], sax["npm_integrity"])
        self.assertEqual(lock["dependencies"]["sax"]["npm_integrity"], sax["npm_integrity"])
        self.assertEqual(self.parser["underlying_parser"]["selected_path"], sax["project"])
        self.assertEqual(self.manifest["afl_coverage_subject_prefix"],
                         "/work/node_modules/sax/lib/sax.js")
        snapshot = read(ROOT / "data/javascript/xml/registry-snapshot.json")
        self.assertEqual(self.parser["popularity"]["value"], snapshot["downloads"]["xml-js"]["value"])

    def test_own_and_underlying_coverage_and_repeatable_feedback(self):
        self.assertEqual(self.receipt["parser_source_files"], 1)
        self.assertGreater(self.receipt["parser_source_lines_covered"], 0)
        self.assertEqual(self.receipt["underlying_source_files"], 1)
        self.assertGreater(self.receipt["underlying_source_lines_covered"], 0)
        result, = read(ROOT / "data/javascript/xml/xml-js-feedback-differential.json")["results"]
        overlay = read(ROOT / "fuzzing/afl-native/xml/javascript/xml_js/verification.json")
        self.assertEqual(result["overlay_receipt_sha256"], sha256((ROOT / "fuzzing/afl-native/xml/javascript/xml_js/verification.json").read_bytes()).hexdigest())
        self.assertEqual(overlay["base_image_id"], self.receipt["image_id"])
        self.assertTrue(result["repeated_control_identical"])
        self.assertTrue(result["repeated_differential_identical"])
        self.assertEqual(result["differential_output"], self.manifest["differential_expected_output"])
        self.assertGreater(result["parser_feature_difference"], 0)
        self.assertGreater(result["afl_tuple_difference"], 0)
        self.assertEqual(set(result["control_only_features_by_file"]), {"sax.js"})
        self.assertEqual(set(result["differential_only_features_by_file"]), {"sax.js"})


if __name__ == "__main__":
    unittest.main()
