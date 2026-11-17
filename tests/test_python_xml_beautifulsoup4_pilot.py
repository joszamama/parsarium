"""The Python XML beautifulsoup4 path keeps its catalog, lock, receipts, and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/xml"
PROJECT = ROOT / "projects/xml/python/beautifulsoup4"
OVERLAY = ROOT / "fuzzing/afl-native/xml/python/beautifulsoup4"
LXML = ROOT / "projects/xml/python/lxml"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PythonXmlBeautifulSoup4PilotTest(unittest.TestCase):
    def test_cell_counts_and_ranked_order(self):
        parsers = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")["leads"]
        cell = read(BASE / "cell.json")
        self.assertEqual([parser["name"] for parser in parsers],
                         ["lxml", "beautifulsoup4", "defusedxml", "xmltodict", "xmlschema", "parsel", "pyquery", "untangle", "jxmlease"])
        downloads = {lead["name"]: lead["last_month"] for lead in leads}
        metrics = [downloads[parser["name"]] for parser in parsers]
        self.assertEqual(metrics, sorted(metrics, reverse=True))
        self.assertEqual(len(parsers), cell["verified_third_party_count"])
        self.assertEqual(sum(lead["status"] == "lead" for lead in leads),
                         cell["unresolved_documentation_leads"])
        lead, = [lead for lead in leads if lead["name"] == "beautifulsoup4"]
        self.assertEqual(lead["status"], "promoted_to_verified")
        parser, = [parser for parser in parsers if parser["name"] == "beautifulsoup4"]
        self.assertEqual(parser["popularity"]["value"], lead["last_month"], 315320831)
        self.assertIn("HTML", parser["popularity"]["limitation"])
        self.assertIn("libxml2 XML parser", parser["shared_families"])
        self.assertIn("not an independent XML tokenizer", parser["verification_note"])

    def test_release_lock_matches_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(BASE / "source-lock.json")
        requirements = (PROJECT / "runtime-requirements.lock").read_text()
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual(lock["beautifulsoup4"]["sha256"], manifest["source_sha256"])
        self.assertEqual(lock["beautifulsoup4"]["sdist_sha256"], manifest["sdist_sha256"])
        self.assertIn(f"beautifulsoup4==4.15.0 --hash=sha256:{manifest['source_sha256']}", requirements)
        for dependency in manifest["dependencies"]:
            self.assertIn(f"{dependency['package']}=={dependency['release']} --hash=sha256:{dependency['sha256']}",
                          requirements)
            self.assertIn(dependency["sha256"], dockerfile)
        for digest in (manifest["source_sha256"], manifest["sdist_sha256"],
                       manifest["underlying_source_sha256"], manifest["underlying_lxml_source_sha256"],
                       lock["beautifulsoup4"]["license_sha256"]):
            self.assertIn(digest, dockerfile)
        # Same lxml/libxml2 pins as the lxml path.
        lxml = read(LXML / "manifest.json")
        self.assertEqual(manifest["underlying_lxml_source_sha256"], lxml["source_sha256"])
        self.assertEqual(manifest["underlying_source_sha256"], lxml["underlying_source_sha256"])
        self.assertIn("LXMLTreeBuilderForXML", dockerfile)
        self.assertIn('BeautifulSoup(data, "xml")', (PROJECT / "harness.py").read_text())

    def test_project_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "beautifulsoup4"]
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], parser["expected_output"])
        self.assertEqual(manifest["differential_expected_output"], parser["differential_expected_output"])
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        for control, digest in ((manifest["control"], manifest["control_sha256"]),
                                (manifest["differential_control"], manifest["differential_control_sha256"])):
            self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        record, = [item for item in read(BASE / "verification.json")["third_party"]
                   if item["package"] == "beautifulsoup4"]
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(record["output"], receipt["output"])

    def test_tree_summary_matches_lxml_on_shared_fields(self):
        manifest = read(PROJECT / "manifest.json")
        lxml = read(LXML / "manifest.json")
        for key in ("expected_output", "differential_expected_output"):
            shared = {name: manifest[key][name] for name in lxml[key]}
            self.assertEqual(shared, lxml[key])
        self.assertEqual(manifest["differential_expected_output"]["comments"], ["order receipt"])
        self.assertEqual(manifest["differential_expected_output"]["processing_instructions"],
                         ['audit step="1"'])

    def test_feedback_is_stable_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / "beautifulsoup4-valid-feedback.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["tested_builder"], "bs4.builder._lxml.LXMLTreeBuilderForXML")
        self.assertTrue(report["pass"] and report["control_repeat_identical"]
                        and report["variant_repeat_identical"])
        self.assertEqual(report["control_output"], manifest["expected_output"])
        self.assertEqual(report["variant_output"], manifest["differential_expected_output"])
        self.assertGreater(report["bs4_feature_difference"], 0)
        self.assertGreater(report["libxml2_feature_difference"], 0)
        self.assertGreater(report["afl_tuple_difference"], 0)
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(report["control_parser_features"],
                         report["control_bs4_features"] + report["control_libxml2_features"])


if __name__ == "__main__":
    unittest.main()
