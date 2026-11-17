"""saloonphp/xml-wrangler's raw-name Element summary matches an independent expat oracle on both controls."""

from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/xml"
PROJECT = ROOT / "projects/xml/php/saloon_xml_wrangler"
OVERLAY = ROOT / "fuzzing/afl-native/xml/php/saloon_xml_wrangler"
ROW = BASE / "parsers.json"
FEEDBACK = BASE / "saloonphp-xml-wrangler-feedback-differential.json"

sys.path.insert(0, str(PROJECT))
from oracle import summarize  # noqa: E402


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class PhpXmlSaloonXmlWranglerTest(unittest.TestCase):
    def test_both_controls_match_expat_oracle_at_raw_name_scope(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        target = read(PROJECT / "target.json")["expected_output_by_control_sha256"]
        row, = [item for item in read(ROW) if item["name"] == "saloonphp/xml-wrangler"]
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
            self.assertEqual(oracle, row[output_key])
            self.assertEqual(target[manifest[hash_key]], oracle)
        self.assertEqual(set(target), {manifest["control_sha256"], manifest["differential_control_sha256"]})
        self.assertEqual({row["control"], row["differential_control"]},
                         {"controls/xml/catalog-ns.xml", "controls/xml/order-default-ns.xml"})
        self.assertTrue(feedback["control_output_matches_oracle"])
        self.assertTrue(feedback["differential_output_matches_oracle"])
        self.assertTrue(feedback["file_and_stream_api_match"])

    def test_raw_namespace_behavior_is_recorded_not_repaired(self):
        manifest = read(PROJECT / "manifest.json")
        feedback = read(FEEDBACK)
        row, = [item for item in read(ROW) if item["name"] == "saloonphp/xml-wrangler"]
        order = manifest["differential_expected_output"]
        self.assertIn("plain", order["elements"])
        self.assertNotIn("plain xmlns=", " ".join(order["namespace_declarations"]))
        self.assertTrue(all(":" not in name or name.startswith("p:") for name in order["elements"]))
        self.assertFalse(any(name.startswith("{") for name in order["elements"]))
        self.assertEqual(feedback["raw_package_view_differential"]["plain_attributes"], [])
        self.assertEqual(feedback["raw_package_view_differential"]["values"],
                         {"order": {"line": [{"sku": "A-7", "p:amount": "12.50 €"}, {"plain": {"leaf": ""}}]}})
        self.assertFalse(row["namespace_resolution"])
        summary = (PROJECT / "summary.php").read_text()
        for marker in ("namespaceURI", "lookupNamespace", "DOMDocument", "registerNamespace"):
            self.assertNotIn(marker, summary)

    def test_release_lock_archives_and_adoption_are_pinned(self):
        row, = [item for item in read(ROW) if item["name"] == "saloonphp/xml-wrangler"]
        manifest = read(PROJECT / "manifest.json")
        locks = read(PROJECT / "source-lock.json")
        composer = {item["name"]: item for item in read(PROJECT / "composer.lock")["packages"]}
        dockerfile = (PROJECT / "Dockerfile").read_text()
        lock = locks["saloonphp/xml-wrangler"]
        self.assertEqual((row["version"], manifest["release"], composer["saloonphp/xml-wrangler"]["version"]),
                         (lock["release"],) * 3)
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        self.assertEqual(manifest["catalog_parser"], str(ROW.relative_to(ROOT)))
        self.assertEqual(set(composer), {name for name in locks if "/" in name})
        for name, package in composer.items():
            pinned = locks[name]
            self.assertEqual(package["version"], pinned["release"])
            self.assertEqual(package["source"]["reference"], pinned["composer_reference"])
            self.assertEqual(package["dist"]["reference"], pinned["composer_reference"])
            self.assertEqual(package["license"], ["MIT"])
            self.assertEqual(pinned["license"], "MIT")
            self.assertIn(f"{pinned['composer_reference']} {pinned['source_sha256']}", dockerfile)
            self.assertEqual(pinned["archive_url"].rsplit("/", 1)[1], pinned["composer_reference"])
        self.assertEqual(manifest["underlying_package_source_sha256"], locks["veewee/xml"]["source_sha256"])
        self.assertIn("diff -r", dockerfile)
        self.assertIn(lock["composer_reference"], row["license_evidence"])
        snapshot = read(BASE / "registry-snapshot.json")
        hits = {hit["downloads"] for query in snapshot["search"] for hit in query["hits"]
                if hit["name"] == "saloonphp/xml-wrangler"}
        self.assertEqual(hits, {row["popularity"]["value"]})
        self.assertEqual(row["popularity"]["captured_at_utc"], snapshot["captured_at_utc"])
        self.assertEqual(row["popularity"]["metric"], "Packagist total package downloads")
        self.assertGreaterEqual(row["popularity"]["recheck"]["total"], row["popularity"]["value"])

    def test_coverage_and_native_afl_feedback_are_parser_scoped_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        overlay = read(OVERLAY / "verification.json")
        feedback = read(FEEDBACK)
        self.assertEqual(manifest["coverage_subject_prefix"], "/work/vendor/saloonphp/xml-wrangler/")
        self.assertEqual(manifest["underlying_coverage_subject_prefix"], "/work/vendor/veewee/xml/")
        self.assertEqual(sum(feedback["control_source_lines_by_file"].values()),
                         receipt["parser_source_lines_covered"])
        self.assertEqual(feedback["control_source_lines_by_file"]["src/XmlReader.php"],
                         receipt["format_specific_source_lines_covered"])
        self.assertEqual(feedback["control_underlying_source_lines"], receipt["underlying_source_lines_covered"])
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
            "libxml2-2.15.4/build/.libs/libxml2_la-xmlreader.o",
            "php-8.5.12/ext/dom/document.o",
            "php-8.5.12/ext/xmlreader/php_xmlreader.o"])
        self.assertTrue(overlay["all_repeats_identical"])
        self.assertTrue(overlay["elements_only_maps_equal_full_harness"])
        self.assertEqual(overlay["post_elements_edges"], 0)
        self.assertTrue(overlay["reader_pass_edges_outside_full_harness_identical"])
        self.assertGreater(overlay["reader_pass_tuple_difference"], 0)
        self.assertEqual(feedback["control_afl_tuples"], overlay["feedback_edges"])
        self.assertEqual(feedback["differential_afl_tuples"], overlay["differential_feedback_edges"])
        self.assertEqual(feedback["afl_tuple_difference"], overlay["afl_tuple_difference"])
        self.assertGreater(feedback["afl_tuple_difference"], 0)
        self.assertTrue(feedback["repeated_control_identical"] and feedback["repeated_differential_identical"])
        self.assertIn("libxml2", overlay["shared_family"])

    def test_harness_uses_documented_string_api(self):
        harness = (PROJECT / "harness.php").read_text()
        self.assertIn("XmlReader::fromString($bytes)->elements()", harness)
        runner = (PROJECT / "run-control.php").read_text()
        self.assertIn("XmlReader::fromFile(", runner)
        self.assertIn("XmlReader::fromStream(", runner)
        self.assertIn("parsarium_parse", (PROJECT / "fuzz-target.php").read_text())


if __name__ == "__main__":
    unittest.main()
