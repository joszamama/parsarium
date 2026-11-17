"""The Python XML defusedxml path keeps its catalog, lock, oracle check, receipts, and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/xml"
PROJECT = ROOT / "projects/xml/python/defusedxml"
OVERLAY = ROOT / "fuzzing/afl-native/xml/python/defusedxml"
LXML = ROOT / "projects/xml/python/lxml"
XMLTODICT = ROOT / "projects/xml/python/xmltodict"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PythonXmlDefusedxmlPilotTest(unittest.TestCase):
    def test_cell_counts_and_family(self):
        parsers = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")["leads"]
        cell = read(BASE / "cell.json")
        self.assertEqual(len(parsers), cell["verified_third_party_count"])
        self.assertEqual(sum(lead["status"] == "lead" for lead in leads),
                         cell["unresolved_documentation_leads"])
        lead, = [lead for lead in leads if lead["name"] == "defusedxml"]
        self.assertEqual(lead["status"], "promoted_to_verified")
        parser, = [parser for parser in parsers if parser["name"] == "defusedxml"]
        self.assertEqual(parser["popularity"]["value"], lead["last_month"], 270848271)
        self.assertIn("Expat XML parser", parser["shared_families"])
        self.assertIn("not an independent XML engine", parser["verification_note"])
        families = {item["family"]: item["paths"] for item in read(BASE / "verification.json")["families"]}
        self.assertTrue(any(path.startswith("defusedxml") for path in families["Expat XML parser"]))

    def test_release_lock_matches_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(BASE / "source-lock.json")["defusedxml"]
        requirements = (PROJECT / "runtime-requirements.lock").read_text()
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual(lock["sha256"], manifest["source_sha256"])
        self.assertEqual(lock["sdist_sha256"], manifest["sdist_sha256"])
        self.assertEqual(requirements, f"defusedxml==0.7.1 --hash=sha256:{manifest['source_sha256']}\n")
        for digest in (manifest["source_sha256"], manifest["sdist_sha256"], lock["license_sha256"],
                       manifest["underlying_source_sha256"]):
            self.assertIn(digest, dockerfile)
        # Same Expat pin as the xmltodict path; a nonzero hash seed keeps Expat's salt fixed.
        self.assertEqual(manifest["underlying_source_sha256"],
                         read(XMLTODICT / "manifest.json")["underlying_source_sha256"])
        self.assertIn("ENV PYTHONHASHSEED=1", dockerfile)
        self.assertIn("defusedxml.ElementTree.parse(BytesIO(data))", (PROJECT / "harness.py").read_text())

    def test_project_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "defusedxml"]
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
                   if item["package"] == "defusedxml"]
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(record["output"], receipt["output"])

    def test_outputs_equal_lxml_without_declaration_count(self):
        manifest = read(PROJECT / "manifest.json")
        lxml = read(LXML / "manifest.json")
        report = read(BASE / "defusedxml-valid-feedback.json")
        self.assertEqual((manifest["control"], manifest["differential_control"]),
                         (lxml["control"], lxml["differential_control"]))
        self.assertTrue(report["defusedxml_matches_oracle"]
                        and report["oracle_matches_lxml_path_without_declaration_count"]
                        and report["oracle_name_uris_equal_declared_uris"])
        self.assertEqual(report["oracle_image_id"], read(LXML / "verification.json")["image_id"])
        for key in ("expected_output", "differential_expected_output"):
            theirs = {field: value for field, value in lxml[key].items() if field != "namespace_declarations"}
            self.assertEqual(manifest[key], theirs)

    def test_feedback_is_stable_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / "defusedxml-valid-feedback.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["tested_parser"], "defusedxml.ElementTree.DefusedXMLParser")
        self.assertEqual(report["expat_version"], "expat_2.10.0")
        self.assertTrue(report["pass"] and report["control_repeat_identical"]
                        and report["variant_repeat_identical"])
        self.assertEqual(report["control_output"], manifest["expected_output"])
        self.assertEqual(report["variant_output"], manifest["differential_expected_output"])
        self.assertGreater(report["expat_feature_difference"], 0)
        self.assertGreater(report["afl_tuple_difference"], 0)
        # defusedxml's own guard-installation lines do not vary on valid, DOCTYPE-free controls.
        self.assertEqual(report["package_feature_difference"], 0)
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(report["control_parser_features"],
                         report["control_package_features"] + report["control_elementtree_driver_features"]
                         + report["control_expat_features"])


if __name__ == "__main__":
    unittest.main()
