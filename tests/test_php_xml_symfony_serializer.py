"""The symfony/serializer XmlEncoder::decode path keeps its oracle, pins, adoption and feedback receipts consistent."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/xml"
PROJECT = ROOT / "projects/xml/php/symfony_serializer"
OVERLAY = ROOT / "fuzzing/afl-native/xml/php/symfony_serializer"
PACKAGE = "symfony/serializer"

_spec = importlib.util.spec_from_file_location("symfony_serializer_overlay", OVERLAY / "build.py")
_overlay = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_overlay)
oracle = _overlay.oracle


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PhpXmlSymfonySerializerTest(unittest.TestCase):
    def setUp(self):
        self.manifest = read(PROJECT / "manifest.json")
        self.parser, = read(ROOT / self.manifest["catalog_parser"])

    def test_both_controls_match_the_qualified_name_oracle(self):
        target = read(PROJECT / "target.json")["expected_by_control_sha256"]
        for control, digest, expected in (
                ("control", "control_sha256", "expected_output"),
                ("differential_control", "differential_control_sha256", "differential_expected_output")):
            data = (ROOT / self.manifest[control]).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), self.manifest[digest])
            self.assertEqual(oracle(data), self.manifest[expected])
            self.assertEqual(target[self.manifest[digest]], self.manifest[expected])
        self.assertEqual(len(target), 2)
        self.assertEqual(self.parser["expected_output"], self.manifest["expected_output"])
        # Namespaces reach the summary only as the root's declarations; the nested xmlns="" is not one.
        self.assertEqual(self.manifest["differential_expected_output"]["root_namespaces"],
                         {"": "urn:parsarium:order", "p": "urn:parsarium:price"})

    def test_release_license_and_sources_are_pinned_in_both_images(self):
        lock = read(PROJECT / "source-lock.json")
        entry = lock[PACKAGE]
        self.assertEqual((entry["release"], entry["source_sha256"], entry["license"]),
                         (self.manifest["release"], self.manifest["source_sha256"], "MIT"))
        self.assertEqual((self.parser["version"], self.parser["license"]), (entry["release"], entry["license"]))
        self.assertIn(entry["git_reference"], self.parser["license_evidence"])
        for dockerfile in (PROJECT / "Dockerfile", OVERLAY / "Dockerfile"):
            text = dockerfile.read_text()
            self.assertIn(self.manifest["base_image"], text)
            self.assertIn(entry["license_file_sha256"], text)
            for name in (PACKAGE, "symfony/deprecation-contracts", "symfony/polyfill-ctype"):
                self.assertIn(lock[name]["source_sha256"], text)
                self.assertIn(lock[name]["git_reference"], text)
        overlay = (OVERLAY / "Dockerfile").read_text()
        for field in ("underlying_source_sha256", "php_source_sha256"):
            self.assertIn(self.manifest[field], overlay)

    def test_adoption_is_the_within_php_registry_snapshot_value(self):
        snapshot = read(BASE / "registry-snapshot.json")
        hits = {hit["downloads"] for query in snapshot["search"] for hit in query["hits"] if hit["name"] == PACKAGE}
        popularity = self.parser["popularity"]
        self.assertEqual(hits, {popularity["value"]})
        self.assertEqual(popularity["captured_at_utc"], snapshot["captured_at_utc"])
        self.assertEqual(popularity["snapshot"], "data/php/xml/registry-snapshot.json")
        self.assertIn("not XML-decoding uses", popularity["caveat"])

    def test_receipts_record_package_lines_and_parse_time_feedback(self):
        project = read(PROJECT / "verification.json")
        overlay = read(OVERLAY / "verification.json")
        self.assertTrue(project["pass"] and overlay["pass"])
        self.assertEqual(project["output"], self.manifest["expected_output"])
        for name, digest in project["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        lines = overlay["package_line_coverage"]
        self.assertEqual(project["format_specific_source_lines_covered"], lines["control_lines"])
        self.assertTrue(lines["control_only_lines"] and lines["differential_only_lines"])
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(overlay["base_image_id"], project["image_id"])
        self.assertEqual(overlay["instrumented_objects"], _overlay.INSTRUMENTED_OBJECTS)
        self.assertNotIn("php-8.5.12/ext/libxml/libxml.o", overlay["instrumented_objects"])
        self.assertTrue(overlay["all_repeats_identical"] and overlay["post_parse_edges_identical"])
        self.assertGreater(overlay["format_dependent_parse_time_tuples"], 0)
        self.assertEqual(overlay["format_dependent_traversal_only_tuples"], 0)
        self.assertEqual(overlay["afl_tuple_difference"], overlay["parse_only_tuple_difference"])
        for name in ("Dockerfile", "build.py"):
            self.assertEqual(overlay["overlay_file_sha256"][name], sha256((OVERLAY / name).read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
