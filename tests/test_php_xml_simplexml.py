"""The PHP simplexml_load_string standard path keeps its oracle, pins and feedback receipts consistent."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/xml"
PROJECT = ROOT / "projects/xml/php/stdlib_simplexml"
OVERLAY = ROOT / "fuzzing/afl-native/xml/php/stdlib_simplexml"
API = ("simplexml_load_string(string $data, ?string $class_name = SimpleXMLElement::class, int $options = 0, "
       "string $namespace_or_prefix = \"\", bool $is_prefix = false)")

_spec = importlib.util.spec_from_file_location("xml_check_controls", ROOT / "controls/xml/check_controls.py")
_oracle = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_oracle)
summarize = _oracle.summarize


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PhpXmlSimpleXmlTest(unittest.TestCase):
    def setUp(self):
        self.manifest = read(PROJECT / "manifest.json")

    def test_both_controls_match_the_expat_oracle(self):
        target = read(PROJECT / "target.json")["expected_by_control_sha256"]
        for control, digest, expected in (
                ("control", "control_sha256", "expected_output"),
                ("differential_control", "differential_control_sha256", "differential_expected_output")):
            data = (ROOT / self.manifest[control]).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), self.manifest[digest])
            self.assertEqual(summarize(data), self.manifest[expected])
            self.assertEqual(target[self.manifest[digest]], self.manifest[expected])
        self.assertEqual(len(target), 2)

    def test_standard_inventory_lists_simplexml_as_verified_and_unranked(self):
        standard = read(BASE / "standard.json")
        entry, = [api for api in standard["verified_apis"] if api["api"] == API]
        self.assertEqual(entry["runtime"], self.manifest["runtime"])
        self.assertEqual(entry["expected"], self.manifest["expected_output"])
        self.assertEqual(entry["differential_expected"], self.manifest["differential_expected_output"])
        self.assertNotIn(API, {api["api"] for api in standard["unverified_documented_apis"]})
        self.assertEqual(read(BASE / "cell.json")["verified_standard_or_runtime_count"], len(standard["verified_apis"]))
        self.assertNotIn("php-simplexml", {parser["name"] for parser in read(BASE / "parsers.json")})

    def test_sources_and_licenses_are_pinned_in_both_images(self):
        for dockerfile in (PROJECT / "Dockerfile", OVERLAY / "Dockerfile"):
            text = dockerfile.read_text()
            for field in ("base_image", "source_sha256", "underlying_source_sha256", "fuzz_engine_sha256"):
                self.assertIn(self.manifest[field], text)
            self.assertIn("sha256sum php-8.5.12/LICENSE libxml2-2.15.4/Copyright", text)
            self.assertIn("sha256sum php-8.5.12/ext/simplexml/simplexml.c php-8.5.12/ext/simplexml/php_simplexml.h", text)
            self.assertIn("--enable-simplexml", text)
        self.assertEqual(read(PROJECT / "runtime-lock.json"),
                         {key: self.manifest[key] for key in ("runtime", "base_image", "source_sha256")})

    def test_receipts_record_parse_time_feedback(self):
        project = read(PROJECT / "verification.json")
        overlay = read(OVERLAY / "verification.json")
        self.assertTrue(project["pass"] and overlay["pass"])
        self.assertEqual(project["output"], self.manifest["expected_output"])
        self.assertGreater(project["format_specific_source_lines_covered"], 0)
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(overlay["instrumented_objects"][-1], "php-8.5.12/ext/simplexml/simplexml.o")
        self.assertNotIn("php-8.5.12/ext/libxml/libxml.o", overlay["instrumented_objects"])
        self.assertEqual(overlay["extension_source_sha256"], self.manifest["extension_source_sha256"])
        # The fuzz target only loads; edges it reaches outside the traversal harness must not depend on input.
        self.assertTrue(overlay["all_repeats_identical"] and overlay["parse_only_edges_outside_full_harness_identical"])
        self.assertGreater(overlay["afl_tuple_difference"], 0)
        for name in ("Dockerfile", "build.py"):
            self.assertEqual(overlay["overlay_file_sha256"][name], sha256((OVERLAY / name).read_bytes()).hexdigest())
        row, = [item for item in read(BASE / "afl-feedback.json")["results"]
                if item["project"] == "xml/php/stdlib_simplexml"]
        self.assertEqual(row["overlay_receipt_sha256"], sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(row["control_afl_tuples"], overlay["feedback_edges"])


if __name__ == "__main__":
    unittest.main()
