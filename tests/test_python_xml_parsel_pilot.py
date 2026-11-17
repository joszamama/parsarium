"""The selected Python XML parsel path keeps its row, lock, receipts, oracle and feedback consistent."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/xml"
PROJECT = ROOT / "projects/xml/python/parsel"
OVERLAY = ROOT / "fuzzing/afl-native/xml/python/parsel"
LXML = ROOT / "projects/xml/python/lxml"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PythonXmlParselPilotTest(unittest.TestCase):
    def test_selected_row_matches_lead_and_manifest(self):
        row, = [item for item in read(BASE / "parsers.json") if item["name"] == "parsel"]
        manifest = read(PROJECT / "manifest.json")
        lead, = [lead for lead in read(BASE / "leads.json")["leads"] if lead["name"] == "parsel"]
        self.assertEqual(lead["status"], "promoted_to_verified")
        self.assertEqual(manifest["catalog_parser"], "data/python/xml/parsers.json")
        self.assertEqual((row["name"], row["version"]), (manifest["package"], manifest["release"]))
        self.assertEqual(row["popularity"]["value"], lead["last_month"], 3699459)
        self.assertIn("Selector(body=local XML bytes, type='xml')", lead["api_hint"])
        self.assertEqual(row["expected_output"], manifest["expected_output"])
        self.assertEqual(row["differential_expected_output"], manifest["differential_expected_output"])
        self.assertIn("libxml2 XML parser", row["shared_families"])
        self.assertIn("not an independent XML tokenizer", row["verification_note"])
        libxml2 = next(item for item in read(BASE / "verification.json")["families"]
                       if item["family"].startswith("libxml2"))
        self.assertTrue(any(path.startswith("parsel") for path in libxml2["paths"]))

    def test_release_lock_matches_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(BASE / "source-lock.json")["parsel"]
        self.assertEqual((lock["sha256"], lock["sdist_sha256"], lock["license_sha256"]),
                         (manifest["source_sha256"], manifest["sdist_sha256"], manifest["license_sha256"]))
        requirements = (PROJECT / "runtime-requirements.lock").read_text()
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertIn(f"parsel==1.12.1 --hash=sha256:{manifest['source_sha256']}", requirements)
        for dependency in manifest["dependencies"]:
            self.assertIn(f"{dependency['package']}=={dependency['release']} --hash=sha256:{dependency['sha256']}",
                          requirements)
            self.assertIn(dependency["sha256"], dockerfile)
        for digest in (manifest["source_sha256"], manifest["sdist_sha256"], manifest["license_sha256"],
                       manifest["underlying_source_sha256"], manifest["underlying_lxml_source_sha256"]):
            self.assertIn(digest, dockerfile)
        lxml = read(LXML / "manifest.json")
        self.assertEqual(manifest["underlying_lxml_source_sha256"], lxml["source_sha256"])
        self.assertEqual(manifest["underlying_source_sha256"], lxml["underlying_source_sha256"])
        self.assertIn('Selector(body=data, type="xml")', (PROJECT / "harness.py").read_text())

    def test_project_receipt_matches_manifest(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        for control, digest in ((manifest["control"], manifest["control_sha256"]),
                                (manifest["differential_control"], manifest["differential_control_sha256"])):
            self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        record, = [item for item in read(BASE / "verification.json")["third_party"] if item["package"] == "parsel"]
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(record["output"], receipt["output"])
        self.assertEqual(record["differential_output"], manifest["differential_expected_output"])

    def test_expat_oracle_matches_both_controls(self):
        spec = importlib.util.spec_from_file_location("parsel_oracle", PROJECT / "oracle.py")
        oracle = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(oracle)
        manifest = read(PROJECT / "manifest.json")
        self.assertEqual(oracle.summarize((ROOT / manifest["control"]).read_bytes()),
                         manifest["expected_output"])
        self.assertEqual(oracle.summarize((ROOT / manifest["differential_control"]).read_bytes()),
                         manifest["differential_expected_output"])

    def test_summary_matches_lxml_on_shared_fields(self):
        manifest = read(PROJECT / "manifest.json")
        lxml = read(LXML / "manifest.json")
        for key in ("expected_output", "differential_expected_output"):
            self.assertEqual({name: manifest[key][name] for name in lxml[key]}, lxml[key])

    def test_feedback_is_stable_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / "parsel-valid-feedback.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["tested_parser"], "parsel.selector.SafeXMLParser")
        self.assertEqual(report["tested_parser_base"], "lxml.etree.XMLParser")
        self.assertTrue(report["pass"] and report["control_repeat_identical"]
                        and report["variant_repeat_identical"])
        self.assertTrue(report["oracle_matches_control"] and report["oracle_matches_variant"])
        self.assertEqual(report["control_output"], manifest["expected_output"])
        self.assertEqual(report["variant_output"], manifest["differential_expected_output"])
        self.assertGreater(report["libxml2_feature_difference"], 0)
        self.assertGreater(report["afl_tuple_difference"], 0)
        # Recorded, not required: Parsel's own lines do not depend on these valid inputs.
        self.assertEqual(report["parsel_feature_difference"], 0)
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(report["control_parser_features"],
                         report["control_parsel_features"] + report["control_libxml2_features"])


if __name__ == "__main__":
    unittest.main()
