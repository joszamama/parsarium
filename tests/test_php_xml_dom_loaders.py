"""PHP XML DOM-loader wrapper paths (QueryPath, laminas-xml, xml-common, DiDOM) keep their oracle, pins, adoption and feedback consistent."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/xml"
PATHS = {
    "querypath": ("querypath/querypath", "src/QueryPath/DOMQuery.php", "MIT"),
    "laminas_xml": ("laminas/laminas-xml", "src/Security.php", "BSD-3-Clause"),
    "simplesamlphp_xml_common": ("simplesamlphp/xml-common", "src/XML/DOMDocumentFactory.php", "LGPL-2.1-or-later"),
    "didom": ("imangazaliev/didom", "src/DiDom/Document.php", "MIT"),
}

_spec = importlib.util.spec_from_file_location("xml_check_controls", ROOT / "controls/xml/check_controls.py")
oracle = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(oracle)


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def selected(slug: str) -> bool:
    return any(item["name"] == PATHS[slug][0] for item in read(BASE / "parsers.json"))


class PhpXmlDomLoaderTest(unittest.TestCase):
    def slugs(self):
        return [slug for slug in PATHS if selected(slug)]

    def test_both_controls_match_the_namespace_oracle(self):
        for slug in self.slugs():
            with self.subTest(slug=slug):
                project = ROOT / "projects/xml/php" / slug
                manifest = read(project / "manifest.json")
                target = read(project / "target.json")["expected_by_control_sha256"]
                for control, digest, expected in (
                        ("control", "control_sha256", "expected_output"),
                        ("differential_control", "differential_control_sha256", "differential_expected_output")):
                    data = (ROOT / manifest[control]).read_bytes()
                    self.assertEqual(sha256(data).hexdigest(), manifest[digest])
                    self.assertEqual(oracle.summarize(data), manifest[expected])
                    self.assertEqual(target[manifest[digest]], manifest[expected])

    def test_release_and_sources_are_pinned_in_both_images(self):
        for slug in self.slugs():
            with self.subTest(slug=slug):
                package, converter, license_id = PATHS[slug]
                project = ROOT / "projects/xml/php" / slug
                overlay = ROOT / "fuzzing/afl-native/xml/php" / slug
                manifest = read(project / "manifest.json")
                entry = read(project / "source-lock.json")[package]
                parser, = [item for item in read(BASE / "parsers.json") if item["name"] == package]
                self.assertEqual((entry["release"], entry["source_sha256"], entry["license"]),
                                 (manifest["release"], manifest["source_sha256"], license_id))
                self.assertEqual((parser["version"], parser["license"]), (entry["release"], entry["license"]))
                for dockerfile in (project / "Dockerfile", overlay / "Dockerfile"):
                    text = dockerfile.read_text()
                    for pinned in (manifest["base_image"], entry["license_file_sha256"], entry["source_sha256"],
                                   entry["git_reference"], entry["file_sha256"][converter]):
                        self.assertIn(pinned, text)
                text = (overlay / "Dockerfile").read_text()
                for field in ("underlying_source_sha256", "php_source_sha256"):
                    self.assertIn(manifest[field], text)

    def test_adoption_is_the_within_php_registry_snapshot_value(self):
        snapshot = read(BASE / "registry-snapshot.json")
        for slug in self.slugs():
            with self.subTest(slug=slug):
                package = PATHS[slug][0]
                parser, = [item for item in read(BASE / "parsers.json") if item["name"] == package]
                hits = {hit["downloads"] for query in snapshot["search"] for hit in query["hits"] if hit["name"] == package}
                self.assertEqual(hits, {parser["popularity"]["value"]})
                self.assertEqual(parser["popularity"]["captured_at_utc"], snapshot["captured_at_utc"])

    def test_receipts_record_parse_time_feedback(self):
        report = {row["project"]: row for row in read(BASE / "afl-feedback.json")["results"]}
        for slug in self.slugs():
            with self.subTest(slug=slug):
                project = ROOT / "projects/xml/php" / slug
                overlay = ROOT / "fuzzing/afl-native/xml/php" / slug
                receipt = read(project / "verification.json")
                afl = read(overlay / "verification.json")
                self.assertTrue(receipt["pass"] and afl["pass"])
                for name, digest in receipt["project_file_sha256"].items():
                    self.assertEqual(sha256((project / name).read_bytes()).hexdigest(), digest, name)
                self.assertEqual(afl["base_project_receipt_sha256"],
                                 sha256((project / "verification.json").read_bytes()).hexdigest())
                self.assertEqual(afl["base_image_id"], receipt["image_id"])
                self.assertNotIn("php-8.5.12/ext/libxml/libxml.o", afl["instrumented_objects"])
                self.assertTrue(afl["all_repeats_identical"] and afl["post_parse_edges_identical"])
                self.assertGreater(afl["format_dependent_parse_time_tuples"], 0)
                self.assertEqual(afl["format_dependent_traversal_only_tuples"], 0)
                # Wrapper path: the package's own lines are the same on both controls.
                self.assertFalse(afl["package_line_coverage"]["package_lines_differ"])
                for name in ("Dockerfile", "build.py"):
                    self.assertEqual(afl["overlay_file_sha256"][name], sha256((overlay / name).read_bytes()).hexdigest())
                row = report[f"xml/php/{slug}"]
                self.assertEqual(row["overlay_receipt_sha256"], sha256((overlay / "verification.json").read_bytes()).hexdigest())
                self.assertGreater(row["afl_tuple_difference"], 0)


if __name__ == "__main__":
    unittest.main()
