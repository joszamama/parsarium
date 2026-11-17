"""The veewee/xml xml_decode path keeps its oracle, pins, adoption and feedback receipts consistent."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/xml"
PROJECT = ROOT / "projects/xml/php/veewee_xml"
OVERLAY = ROOT / "fuzzing/afl-native/xml/php/veewee_xml"
PACKAGE = "veewee/xml"

_spec = importlib.util.spec_from_file_location("veewee_xml_overlay", OVERLAY / "build.py")
_overlay = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_overlay)
oracle = _overlay.oracle


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PhpXmlVeeweeTest(unittest.TestCase):
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
            # Qualified names plus per-element declarations resolve to the namespace-aware expat names.
            self.assertEqual(_overlay.resolve_summary(self.manifest[expected], data), _overlay.expanded_names(data))
        self.assertEqual(len(target), 2)
        self.assertEqual(self.parser["expected_output"], self.manifest["expected_output"])
        # The nested default-namespace undeclaration on <plain> is exposed.
        self.assertIn("5 plain xmlns=", self.manifest["differential_expected_output"]["namespace_declarations"])

    def test_release_license_lock_and_archives_are_pinned_in_both_images(self):
        lock = read(PROJECT / "source-lock.json")
        entry = lock[PACKAGE]
        self.assertEqual((entry["release"], entry["source_sha256"], entry["license"]),
                         (self.manifest["release"], self.manifest["source_sha256"], "MIT"))
        self.assertEqual((self.parser["version"], self.parser["license"]), (entry["release"], entry["license"]))
        self.assertIn(entry["git_reference"], self.parser["license_evidence"])
        composer_lock_bytes = (PROJECT / "composer.lock").read_bytes()
        self.assertEqual(sha256(composer_lock_bytes).hexdigest(), entry["composer_lock_sha256"])
        composer_lock = json.loads(composer_lock_bytes)
        self.assertEqual(composer_lock["content-hash"], entry["composer_lock_content_hash"])
        archives = {}
        for line in (PROJECT / "vendor-archives.txt").read_text().splitlines():
            if not line.startswith("#"):
                digest, name, version, url = line.split()
                archives[name] = (digest, version, url)
        locked = {package["name"]: package for package in composer_lock["packages"]}
        self.assertEqual(set(archives), set(locked))
        for name, package in locked.items():
            digest, version, url = archives[name]
            self.assertEqual((version, lock[name]["release"]), (package["version"], package["version"]))
            self.assertEqual((digest, url), (lock[name]["source_sha256"], lock[name]["archive_url"]))
            self.assertTrue(url.endswith("/" + package["source"]["reference"]))
            self.assertEqual(package["license"], ["MIT"])
        for dockerfile in (PROJECT / "Dockerfile", OVERLAY / "Dockerfile"):
            text = dockerfile.read_text()
            self.assertIn(self.manifest["base_image"], text)
            self.assertIn(entry["license_file_sha256"], text)
            self.assertIn("vendor-archives.txt", text)
            self.assertIn("sha256sum --check", text)
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
        self.assertIn("not xml_decode uses", popularity["caveat"])

    def test_receipts_record_package_lines_and_load_time_feedback(self):
        project = read(PROJECT / "verification.json")
        overlay = read(OVERLAY / "verification.json")
        self.assertTrue(project["pass"] and overlay["pass"])
        self.assertEqual(project["output"], self.manifest["expected_output"])
        for name, digest in project["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        lines = overlay["package_line_coverage"]
        self.assertEqual(project["parser_source_lines_covered"], lines["control_lines"])
        self.assertEqual(lines["line_sets_identical"],
                         not (lines["control_only_lines"] or lines["differential_only_lines"]))
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(overlay["base_image_id"], project["image_id"])
        self.assertEqual(overlay["instrumented_objects"], _overlay.INSTRUMENTED_OBJECTS)
        for excluded in ("php-8.5.12/ext/libxml/libxml.o", "php-8.5.12/ext/dom/namespace_compat.o"):
            self.assertNotIn(excluded, overlay["instrumented_objects"])
        self.assertTrue(overlay["all_repeats_identical"] and overlay["post_parse_edges_identical"])
        self.assertTrue(overlay["declarations_resolve_to_expanded_names"])
        self.assertGreater(overlay["format_dependent_parse_time_tuples"], 0)
        self.assertEqual(overlay["format_dependent_traversal_only_tuples"], 0)
        self.assertEqual(overlay["afl_tuple_difference"], overlay["parse_only_tuple_difference"])
        for name in ("Dockerfile", "build.py"):
            self.assertEqual(overlay["overlay_file_sha256"][name], sha256((OVERLAY / name).read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
