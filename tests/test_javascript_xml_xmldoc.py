"""The xmldoc candidate keeps its pins, raw-name oracle, and feedback receipts consistent."""

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/xml/javascript/xmldoc"
OVERLAY = ROOT / "fuzzing/afl-native/xml/javascript/xmldoc"
CANDIDATE = ROOT / "data/javascript/xml/xmldoc-candidate.json"
FEEDBACK = ROOT / "data/javascript/xml/xmldoc-feedback-differential.json"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class JavaScriptXmlXmldocTest(unittest.TestCase):
    def test_release_pins_match_lock_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")["xmldoc"]
        npm_lock = read(PROJECT / "package-lock.json")["packages"]
        snapshot = read(ROOT / "data/javascript/xml/registry-snapshot.json")
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual((lock["release"], lock["license"]), ("3.0.0", "MIT"))
        self.assertEqual(lock["source_sha256"], manifest["source_sha256"])
        self.assertEqual(npm_lock["node_modules/xmldoc"]["integrity"], lock["npm_integrity"])
        inspected = snapshot["latest_release_inspection"]["xmldoc"]
        self.assertEqual((inspected["integrity"], inspected["tarball_sha256"]),
                         (lock["npm_integrity"], lock["source_sha256"]))
        sax = lock["dependencies"]["sax"]
        self.assertEqual(npm_lock["node_modules/sax"]["version"], sax["release"])
        self.assertEqual(npm_lock["node_modules/sax"]["integrity"], sax["npm_integrity"])
        self.assertEqual(sax["source_sha256"], manifest["underlying_source_sha256"])
        for digest in (manifest["base_image"], manifest["source_sha256"], sax["source_sha256"]):
            self.assertIn(digest, dockerfile)
        self.assertIn("new XmlDocument(text)", (PROJECT / "adapter.mjs").read_text())

    def test_candidate_row_records_metric_family_and_no_namespace_resolution(self):
        parser, = read(CANDIDATE)
        manifest = read(PROJECT / "manifest.json")
        snapshot = read(ROOT / "data/javascript/xml/registry-snapshot.json")
        downloads = snapshot["downloads"]["xmldoc"]
        self.assertEqual(parser["popularity"]["value"], downloads["value"], 21414489)
        self.assertEqual(parser["popularity"]["source"], downloads["url"])
        self.assertEqual((downloads["start"], downloads["end"]), ("2026-10-17", "2026-11-15"))
        self.assertIs(parser["namespace_resolution"], False)
        self.assertIs(manifest["namespace_resolution"], False)
        self.assertIn("sax", parser["shared_families"])
        self.assertIn("not an XML 1.0 + Namespaces parser", parser["family_note"])
        for key in ("expected_output", "differential_expected_output"):
            self.assertEqual(parser[key], manifest[key])
            # Raw qualified names only: no Clark-notation URIs anywhere in the summary.
            self.assertNotIn("{urn:", json.dumps(manifest[key]))

    def test_expat_oracle_matches_both_controls(self):
        manifest = read(PROJECT / "manifest.json")
        oracle = json.loads(subprocess.run([sys.executable, "-I", str(PROJECT / "oracle.py")],
                                           check=True, capture_output=True, text=True).stdout)
        self.assertEqual(oracle[manifest["control"]], manifest["expected_output"])
        self.assertEqual(oracle[manifest["differential_control"]], manifest["differential_expected_output"])
        self.assertEqual(manifest["expected_output"]["root"], "c:catalog")
        self.assertIn("xmlns=", manifest["differential_expected_output"]["attributes"])
        # The prolog comment of the order control is outside the tree xmldoc keeps.
        self.assertEqual(manifest["differential_expected_output"]["comments"], [])

    def test_project_receipt_pins_files_and_coverage(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        self.assertTrue(receipt["pass"] and receipt["fuzz_engine_smoke_pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        for control, digest in ((manifest["control"], manifest["control_sha256"]),
                                (manifest["differential_control"], manifest["differential_control_sha256"])):
            self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)

    def test_feedback_is_stable_and_differential_in_parser_sources(self):
        overlay = read(OVERLAY / "verification.json")
        report = read(FEEDBACK)
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertTrue(report["pass"] and report["repeated_control_identical"]
                        and report["repeated_differential_identical"])
        self.assertTrue(report["control_output_matches_oracle"] and report["differential_output_matches_oracle"])
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(set(report["control_features_by_package"]), {"xmldoc", "sax"})
        self.assertGreater(report["parser_feature_difference"], 0)
        self.assertGreater(report["afl_tuple_difference"], 0)
        self.assertEqual(set(report["differential_features_by_package"]), {"xmldoc", "sax"})
        changed = {**report["control_only_features_by_file"], **report["differential_only_features_by_file"]}
        self.assertEqual(set(changed), {"xmldoc/dist/index.js", "sax/lib/sax.js"})


if __name__ == "__main__":
    unittest.main()
