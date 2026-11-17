"""The Python XML jxmlease raw-name path keeps its catalog, lock, oracles, receipts and feedback consistent."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/xml"
PROJECT = ROOT / "projects/xml/python/jxmlease"
OVERLAY = ROOT / "fuzzing/afl-native/xml/python/jxmlease"
XMLTODICT = ROOT / "projects/xml/python/xmltodict"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PythonXmlJxmleasePilotTest(unittest.TestCase):
    def test_row_lead_and_snapshot_agree(self):
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "jxmlease"]
        lead, = [lead for lead in read(BASE / "leads.json")["leads"] if lead["name"] == "jxmlease"]
        snapshot = read(BASE / "registry-snapshot.json")
        manifest = read(PROJECT / "manifest.json")
        self.assertEqual(lead["status"], "promoted_to_verified")
        self.assertEqual(parser["popularity"]["value"], lead["last_month"],
                         snapshot["download_metric"]["packages"]["jxmlease"]["downloads"])
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        self.assertEqual(parser["differential_expected_output"], manifest["differential_expected_output"])
        self.assertEqual(parser["shared_families"], ["Expat XML parser"])
        self.assertIn("Raw-name view", parser["verification_note"])
        families = {item["family"]: item["paths"] for item in read(BASE / "verification.json")["families"]}
        self.assertTrue(any(path.startswith("jxmlease") for path in families["Expat XML parser"]))

    def test_release_lock_matches_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(BASE / "source-lock.json")["jxmlease"]
        requirements = (PROJECT / "runtime-requirements.lock").read_text()
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual((lock["sha256"], lock["sdist_sha256"], lock["license_sha256"]),
                         (manifest["source_sha256"], manifest["sdist_sha256"], manifest["license_sha256"]))
        self.assertIn(f"jxmlease==1.0.3 --hash=sha256:{manifest['source_sha256']}", requirements)
        for digest in (manifest["source_sha256"], manifest["sdist_sha256"], manifest["license_sha256"],
                       manifest["underlying_source_sha256"]):
            self.assertIn(digest, dockerfile)
        self.assertEqual(manifest["underlying_source_sha256"],
                         read(XMLTODICT / "manifest.json")["underlying_source_sha256"])
        self.assertIn("ENV PYTHONHASHSEED=1", dockerfile)
        self.assertIn("jxmlease.parse(Path(path).read_bytes())", (PROJECT / "harness.py").read_text())

    def test_project_receipt_matches_catalog(self):
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
        record, = [item for item in read(BASE / "verification.json")["third_party"]
                   if item["package"] == "jxmlease"]
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())

    def test_raw_name_oracle(self):
        spec = importlib.util.spec_from_file_location("raw_oracle", ROOT / "projects/xml/c/libnxml/oracle.py")
        oracle = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(oracle)
        manifest = read(PROJECT / "manifest.json")
        for control, key in ((manifest["control"], "expected_output"),
                             (manifest["differential_control"], "differential_expected_output")):
            self.assertEqual(oracle.summarize((ROOT / control).read_bytes()), manifest[key])
            self.assertFalse(any(name.startswith("{") for name in manifest[key]["elements"]))
        self.assertIn("c:catalog", manifest["expected_output"]["elements"])
        self.assertIn("p:amount", manifest["differential_expected_output"]["elements"])

    def test_feedback_is_stable_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / "jxmlease-valid-feedback.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertTrue(report["pass"] and report["control_repeat_identical"]
                        and report["variant_repeat_identical"])
        self.assertTrue(report["expat_oracle_matches"] and report["lxml_projection_matches"])
        self.assertFalse(report["process_namespaces"])
        self.assertEqual(report["expat_version"], "expat_2.10.0")
        self.assertEqual(report["control_output"], manifest["expected_output"])
        self.assertEqual(report["variant_output"], manifest["differential_expected_output"])
        self.assertGreater(report["expat_feature_difference"], 0)
        self.assertGreater(report["afl_tuple_difference"], 0)
        self.assertEqual(report["jxmlease_feature_difference"], 0)
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(report["control_parser_features"],
                         report["control_jxmlease_features"] + report["control_expat_features"])


if __name__ == "__main__":
    unittest.main()
