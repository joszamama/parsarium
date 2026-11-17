"""pear/xml_parser's raw-name SAX summary matches an independent expat oracle on both controls."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/xml"
PROJECT = ROOT / "projects/xml/php/pear_xml_parser"
OVERLAY = ROOT / "fuzzing/afl-native/xml/php/pear_xml_parser"
ROW = BASE / "parsers.json"
FEEDBACK = BASE / "pear-xml-parser-feedback-differential.json"
NAME = "pear/xml_parser"

# Loaded under its own module name: other XML projects also ship an oracle.py.
_spec = importlib.util.spec_from_file_location("pear_xml_parser_oracle", PROJECT / "oracle.py")
_oracle = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_oracle)
summarize = _oracle.summarize


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def row() -> dict:
    found, = [item for item in read(ROW) if item["name"] == NAME]
    return found


class PhpXmlPearXmlParserTest(unittest.TestCase):
    def test_both_controls_match_expat_oracle_at_raw_name_scope(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        target = read(PROJECT / "target.json")["expected_output_by_control_sha256"]
        record = row()
        feedback = read(FEEDBACK)
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        for control_key, hash_key, output_key in (
                ("control", "control_sha256", "expected_output"),
                ("differential_control", "differential_control_sha256", "differential_expected_output")):
            data = (ROOT / manifest[control_key]).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), manifest[hash_key])
            oracle = summarize(data)
            self.assertEqual(oracle, manifest[output_key])
            self.assertEqual(oracle, record[output_key])
            self.assertEqual(target[manifest[hash_key]], oracle)
        self.assertEqual(set(target), {manifest["control_sha256"], manifest["differential_control_sha256"]})
        self.assertTrue(feedback["control_output_matches_oracle"])
        self.assertTrue(feedback["differential_output_matches_oracle"])
        self.assertTrue(feedback["file_and_stream_api_match"])

    def test_raw_names_and_case_folding_are_recorded_not_repaired(self):
        manifest = read(PROJECT / "manifest.json")
        feedback = read(FEEDBACK)
        order = manifest["differential_expected_output"]
        self.assertIn("xmlns=", order["attributes"])
        self.assertIn("xmlns:p=urn:parsarium:price", order["attributes"])
        self.assertIn("p:amount", order["elements"])
        self.assertFalse(any(name.startswith("{") for name in order["elements"]))
        self.assertEqual(order["processing_instructions"], ['audit step="1"'])
        folding = feedback["default_case_folding_view_differential"]
        self.assertIs(folding["folding_default"], True)
        self.assertEqual(folding["elements"], [name.upper() for name in order["elements"]])
        self.assertFalse(row()["namespace_resolution"])
        summary = (PROJECT / "summary.php").read_text()
        self.assertIn("$parser->folding = false;", summary)
        self.assertNotIn("xml_parser_create_ns", summary)
        self.assertTrue(any("xml_set_object" in item for item in feedback["php_deprecations"]))

    def test_release_lock_archives_and_adoption_are_pinned(self):
        record = row()
        manifest = read(PROJECT / "manifest.json")
        locks = read(PROJECT / "source-lock.json")
        composer = {item["name"]: item for item in read(PROJECT / "composer.lock")["packages"]}
        dockerfile = (PROJECT / "Dockerfile").read_text()
        lock = locks[NAME]
        self.assertEqual((record["version"], manifest["release"], composer[NAME]["version"]), (lock["release"],) * 3)
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        self.assertEqual(set(composer), {name for name in locks if name.startswith("pear/")})
        for name, package in composer.items():
            pinned = locks[name]
            self.assertEqual(package["version"], pinned["release"])
            self.assertEqual(package["source"]["reference"], pinned["composer_reference"])
            self.assertEqual(package["dist"]["reference"], pinned["composer_reference"])
            self.assertEqual(package["dist"]["shasum"], "")
            self.assertEqual(package["license"], [pinned["license"]])
            self.assertIn(f"{pinned['composer_reference']} {pinned['source_sha256']}", dockerfile)
        self.assertIn("diff -r", dockerfile)
        self.assertIn(locks["xdebug"]["source_sha256"], dockerfile)
        self.assertIn(lock["composer_reference"], record["license_evidence"])
        snapshot = read(BASE / "registry-snapshot.json")
        hits = {hit["downloads"] for query in snapshot["search"] for hit in query["hits"] if hit["name"] == NAME}
        self.assertEqual(hits, {record["popularity"]["value"]})
        self.assertEqual(record["popularity"]["captured_at_utc"], snapshot["captured_at_utc"])
        self.assertGreaterEqual(record["popularity"]["recheck"]["total"], record["popularity"]["value"])
        lead, = [item for item in read(BASE / "leads.json") if item["name"] == NAME]
        self.assertEqual((lead["status"], lead["packagist_downloads"]), ("selected", record["popularity"]["value"]))

    def test_package_and_libxml2_lines_and_native_feedback(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        overlay = read(OVERLAY / "verification.json")
        feedback = read(FEEDBACK)
        self.assertEqual(manifest["coverage_subject_prefix"], "/work/vendor/pear/xml_parser/")
        self.assertEqual(manifest["underlying_coverage_subject_prefix"], "/work/source/libxml2-2.15.4/")
        package_lines = feedback["control_package_lines"]["XML/Parser.php"]
        self.assertEqual(len(package_lines), receipt["parser_source_lines_covered"])
        self.assertEqual(receipt["format_specific_source_lines_covered"], receipt["parser_source_lines_covered"])
        self.assertTrue(feedback["package_lines_identical_between_controls"])
        self.assertGreater(receipt["underlying_source_lines_covered"], 1000)
        self.assertGreater(feedback["control_underlying_parser_lines_by_file"]["parser.c"], 0)
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(overlay["base_image_id"], receipt["image_id"])
        self.assertEqual(feedback["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        for name, digest in overlay["overlay_file_sha256"].items():
            self.assertEqual(sha256((OVERLAY / name).read_bytes()).hexdigest(), digest)
        self.assertEqual(overlay["instrumented_objects"], [
            "libxml2-2.15.4/build/.libs/libxml2_la-SAX2.o",
            "libxml2-2.15.4/build/.libs/libxml2_la-parser.o",
            "libxml2-2.15.4/build/.libs/libxml2_la-parserInternals.o",
            "php-8.5.12/ext/xml/compat.o",
            "php-8.5.12/ext/xml/xml.o"])
        self.assertTrue(overlay["all_repeats_identical"])
        self.assertEqual(overlay["format_dependent_harness_only_tuples"], 0)
        self.assertGreater(overlay["afl_tuple_difference"], 0)
        self.assertEqual(feedback["afl_tuple_difference"], overlay["afl_tuple_difference"])
        # The package drives ext/xml but adds no input-dependent native tuples of its own.
        self.assertTrue(overlay["differing_tuples_subset_of_bare_baseline"])
        self.assertEqual(overlay["differing_tuples_package_path_only"], 0)
        self.assertIn("libxml2", overlay["shared_family"])

    def test_harness_uses_documented_input_api(self):
        summary = (PROJECT / "summary.php").read_text()
        for call in ("setInputString($input)", "setInputFile($input)", "setInput($input)",
                     "setHandlerObj($handler)", "$parser->parse()"):
            self.assertIn(call, summary)
        runner = (PROJECT / "run-control.php").read_text()
        self.assertIn("parsarium_xml_parser_summary('file'", runner)
        self.assertIn("parsarium_xml_parser_summary('stream'", runner)
        self.assertIn("parsarium_parse", (PROJECT / "fuzz-target.php").read_text())
        baseline = (OVERLAY / "baseline.php").read_text()
        self.assertNotIn("new XML_Parser", baseline)
        self.assertNotIn("vendor/autoload.php", baseline)


if __name__ == "__main__":
    unittest.main()
