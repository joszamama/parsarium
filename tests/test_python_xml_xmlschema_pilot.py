"""The selected Python XML xmlschema path keeps its pins, oracle, receipts and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/xml"
PROJECT = ROOT / "projects/xml/python/xmlschema"
OVERLAY = ROOT / "fuzzing/afl-native/xml/python/xmlschema"
LXML = ROOT / "projects/xml/python/lxml"
XMLTODICT = ROOT / "projects/xml/python/xmltodict"

def parser_entry() -> dict:
    return next(item for item in read(BASE / "parsers.json") if item["name"] == "xmlschema")


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PythonXmlXmlschemaPilotTest(unittest.TestCase):
    def test_selected_entry_matches_lead_and_family(self):
        parser = parser_entry()
        lead, = [item for item in read(BASE / "leads.json")["leads"] if item["name"] == "xmlschema"]
        self.assertEqual(lead["status"], "promoted_to_verified")
        self.assertEqual(parser["popularity"]["value"], lead["last_month"], 7391962)
        self.assertEqual(parser["popularity"]["observed_on_utc"], "2026-11-17")
        self.assertIn("Expat XML parser", parser["shared_families"])
        self.assertIn("not an independent XML engine", parser["verification_note"])
        expat_family = next(item for item in read(BASE / "verification.json")["families"]
                            if item["family"] == "Expat XML parser")
        self.assertIn("xmlschema", expat_family["paths"][-1])

    def test_release_lock_matches_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        locks = read(BASE / "source-lock.json")
        lock = locks["xmlschema"]
        elementpath = locks["elementpath_for_xmlschema"]
        requirements = (PROJECT / "runtime-requirements.lock").read_text()
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual(lock["sha256"], manifest["source_sha256"])
        self.assertEqual(lock["sdist_sha256"], manifest["sdist_sha256"])
        dependency, = manifest["dependencies"]
        self.assertEqual((dependency["package"], dependency["release"], dependency["sha256"]),
                         ("elementpath", elementpath["release"], elementpath["sha256"]))
        self.assertEqual(requirements,
                         f"elementpath==5.1.4 --hash=sha256:{elementpath['sha256']}\n"
                         f"xmlschema==4.3.2 --hash=sha256:{manifest['source_sha256']}\n")
        for digest in (manifest["source_sha256"], manifest["sdist_sha256"], lock["license_sha256"],
                       elementpath["sha256"], elementpath["sdist_sha256"], elementpath["license_sha256"],
                       manifest["underlying_source_sha256"]):
            self.assertIn(digest, dockerfile)
        # Same Expat pin as the xmltodict path; a nonzero hash seed keeps Expat's salt fixed.
        self.assertEqual(manifest["underlying_source_sha256"],
                         read(XMLTODICT / "manifest.json")["underlying_source_sha256"])
        self.assertIn("ENV PYTHONHASHSEED=1", dockerfile)
        # BytesIO keeps short inputs from being read as URLs or file paths.
        self.assertIn("XMLResource(BytesIO(data))", (PROJECT / "harness.py").read_text())

    def test_project_receipt_matches_selected_record(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser = parser_entry()
        self.assertEqual(manifest["catalog_parser"], "data/python/xml/parsers.json")
        self.assertEqual((parser["name"], parser["version"]), (manifest["package"], manifest["release"]))
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], parser["expected_output"])
        self.assertEqual(manifest["expected_output"], parser["expected_output"])
        self.assertEqual(manifest["differential_expected_output"], parser["differential_expected_output"])
        self.assertEqual(receipt["parser_source_lines_covered"], 110)
        self.assertEqual(receipt["format_specific_source_lines_covered"], 44)
        self.assertEqual(receipt["underlying_source_lines_covered"], 3449)
        for control, digest in ((manifest["control"], manifest["control_sha256"]),
                                (manifest["differential_control"], manifest["differential_control_sha256"])):
            self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        record = next(item for item in read(BASE / "verification.json")["third_party"]
                      if item["package"] == "xmlschema")
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(record["output"], receipt["output"])

    def test_outputs_equal_full_lxml_summary(self):
        manifest = read(PROJECT / "manifest.json")
        lxml = read(LXML / "manifest.json")
        report = read(BASE / "xmlschema-valid-feedback.json")
        self.assertEqual((manifest["control"], manifest["differential_control"]),
                         (lxml["control"], lxml["differential_control"]))
        self.assertTrue(report["xmlschema_matches_oracle"] and report["oracle_matches_lxml_path"]
                        and report["xmlschema_nsmaps_match_lxml_nsmaps"]
                        and report["get_namespaces_uris_equal_declared_uris"])
        self.assertEqual(report["oracle_image_id"], read(LXML / "verification.json")["image_id"])
        for key in ("expected_output", "differential_expected_output"):
            # Unlike defusedxml, the xmlns declaration count is kept: xmlschema records declarations itself.
            self.assertEqual(manifest[key], lxml[key])
        self.assertEqual(report["variant_nsmaps"][-2:], [{"": "", "p": "urn:parsarium:price"}] * 2)

    def test_feedback_is_stable_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / "xmlschema-valid-feedback.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["tested_resource"], "xmlschema.resources.xml_resource.XMLResource")
        self.assertEqual(report["expat_version"], "expat_2.10.0")
        self.assertTrue(report["pass"] and report["control_repeat_identical"]
                        and report["variant_repeat_identical"])
        self.assertEqual(report["control_output"], manifest["expected_output"])
        self.assertEqual(report["variant_output"], manifest["differential_expected_output"])
        self.assertGreater(report["expat_feature_difference"], 0)
        self.assertGreater(report["afl_tuple_difference"], 0)
        # xmlschema runs the same lines on both controls; its namespace bookkeeping differs only in hit-count buckets.
        self.assertEqual(report["package_line_set_difference"], 0)
        self.assertGreater(report["package_feature_difference"], 0)
        self.assertTrue(all(line.startswith("xmlschema/resources/xml_loader.py:")
                            for line in report["package_lines_with_changed_hit_bucket"]))
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(report["control_parser_features"],
                         report["control_package_features"] + report["control_elementtree_driver_features"]
                         + report["control_expat_features"])
        self.assertIn("bucket(hits)", (OVERLAY / "afl_python_trace.py").read_text())


if __name__ == "__main__":
    unittest.main()
