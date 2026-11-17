"""Check the Uppsala XML control and parser-only AFL++ evidence."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/xml/rust/uppsala"
MANIFEST = json.loads((PROJECT / "manifest.json").read_text())
spec = importlib.util.spec_from_file_location("xml_control_oracle", ROOT / "controls/xml/check_controls.py")
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)


class UppsalaEvidenceTest(unittest.TestCase):
    def test_both_controls_match_independent_expat(self):
        for path_key, digest_key, output_key in (
            ("control", "control_sha256", "expected_output"),
            ("afl_variant", "afl_variant_sha256", "afl_variant_expected_output"),
        ):
            data = (ROOT / MANIFEST[path_key]).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), MANIFEST[digest_key])
            self.assertEqual(oracle.summarize(data), MANIFEST[output_key])

    def test_source_pin_and_parser_only_feedback(self):
        lock = tomllib.loads((PROJECT / "Cargo.lock").read_text())
        parser, = [package for package in lock["package"]
                   if package["name"] == "uppsala" and package["version"] == "0.12.1"]
        self.assertEqual(parser["checksum"], MANIFEST["source_sha256"])
        self.assertEqual(MANIFEST["afl_instrumented_crates"], ["uppsala"])
        feedback = json.loads((ROOT / "fuzzing/afl-native/xml/rust/uppsala/verification.json").read_text())
        self.assertEqual(set(feedback["sancov_scope"]["rlib_guard_bytes"]), {"uppsala"})
        self.assertTrue(feedback["control_stability"]["all_repeats_identical"])
        self.assertTrue(feedback["variant_stability"]["all_repeats_identical"])
        self.assertGreater(feedback["edges_only_in_control"], 0)
        self.assertGreater(feedback["edges_only_in_variant"], 0)
        self.assertIn("src/parser.rs", feedback["source_differential"]["files_with_different_line_counts"])


if __name__ == "__main__":
    unittest.main()
