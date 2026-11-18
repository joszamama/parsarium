"""The Python XML Genshi path keeps its catalog, lock, namespace-aware oracles, receipts and feedback consistent."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/xml"
PROJECT = ROOT / "projects/xml/python/genshi"
OVERLAY = ROOT / "fuzzing/afl-native/xml/python/genshi"
XMLTODICT = ROOT / "projects/xml/python/xmltodict"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PythonXmlGenshiPilotTest(unittest.TestCase):
    def test_row_lead_snapshot_and_rank_agree(self):
        parsers = read(BASE / "parsers.json")
        parser, = [item for item in parsers if item["name"] == "genshi"]
        lead, = [lead for lead in read(BASE / "leads.json")["leads"] if lead["name"] == "genshi"]
        snapshot = read(BASE / "registry-snapshot.json")
        manifest = read(PROJECT / "manifest.json")
        self.assertEqual(lead["status"], "promoted_to_verified")
        self.assertEqual(parser["popularity"]["value"], lead["last_month"],
                         snapshot["download_metric"]["packages"]["genshi"]["downloads"])
        self.assertEqual(parser["popularity"]["observed_on_utc"], "2026-11-18")
        self.assertEqual([item["name"] for item in parsers][-2:], ["genshi", "jxmlease"])
        values = [item["popularity"]["value"] for item in parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(len(parsers), cell["ceiling"])
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        self.assertEqual(parser["differential_expected_output"], manifest["differential_expected_output"])
        self.assertEqual(parser["shared_families"], ["Expat XML parser"])
        families = {item["family"]: item["paths"] for item in read(BASE / "verification.json")["families"]}
        self.assertTrue(any(path.startswith("genshi") for path in families["Expat XML parser"]))
        self.assertIn("| 9 | [Genshi]", (BASE / "ranking.md").read_text(encoding="utf-8"))

    def test_round_four_lead_decisions(self):
        leads = {lead["name"]: lead for lead in read(BASE / "leads.json")["leads"]}
        self.assertEqual(leads["suds-community"]["status"], "excluded")
        self.assertEqual(leads["twisted"]["status"], "excluded")
        self.assertEqual(leads["xmltodict-rs"]["status"], "unresolved_below_ceiling")
        self.assertLess(leads["xmltodict-rs"]["last_month"], leads["jxmlease"]["last_month"])
        self.assertEqual(leads["rapidxml"]["status"], "excluded")
        self.assertIn("parse_cdata", leads["rapidxml"]["round_4_recheck"])

    def test_release_lock_matches_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(BASE / "source-lock.json")["genshi"]
        requirements = (PROJECT / "runtime-requirements.lock").read_text()
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual((lock["sha256"], lock["sdist_sha256"]), (manifest["source_sha256"], manifest["sdist_sha256"]))
        self.assertIn(f"genshi==0.7.12 --hash=sha256:{manifest['source_sha256']}", requirements)
        for digest in (manifest["source_sha256"], manifest["sdist_sha256"], lock["license_sha256"],
                       manifest["underlying_source_sha256"]):
            self.assertIn(digest, dockerfile)
        self.assertEqual(manifest["underlying_source_sha256"],
                         read(XMLTODICT / "manifest.json")["underlying_source_sha256"])
        self.assertIn("ENV PYTHONHASHSEED=1", dockerfile)
        self.assertIn("XMLParser(BytesIO(Path(path).read_bytes())", (PROJECT / "harness.py").read_text())

    def test_project_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        record, = [item for item in read(BASE / "verification.json")["third_party"] if item["package"] == "genshi"]
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())

    def test_namespace_aware_oracle(self):
        spec = importlib.util.spec_from_file_location("ns_oracle", ROOT / "controls/xml/check_controls.py")
        oracle = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(oracle)
        manifest = read(PROJECT / "manifest.json")
        lxml = read(ROOT / "projects/xml/python/lxml/manifest.json")
        for control, key in ((manifest["control"], "expected_output"),
                             (manifest["differential_control"], "differential_expected_output")):
            self.assertEqual(oracle.summarize((ROOT / control).read_bytes()), manifest[key])
            self.assertEqual(lxml[key], manifest[key])
        self.assertEqual(manifest["differential_expected_output"]["namespace_declarations"], 3)

    def test_feedback_is_stable_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / "genshi-valid-feedback.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertTrue(report["pass"] and report["control_repeat_identical"] and report["variant_repeat_identical"])
        self.assertTrue(report["expat_oracle_matches"] and report["lxml_path_matches"])
        self.assertEqual(report["expat_version"], "expat_2.10.0")
        self.assertEqual(report["control_output"], manifest["expected_output"])
        self.assertEqual(report["variant_output"], manifest["differential_expected_output"])
        self.assertGreater(report["expat_feature_difference"], report["genshi_feature_difference"])
        self.assertGreater(report["afl_tuple_difference"], 0)
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(report["control_parser_features"],
                         report["control_genshi_features"] + report["control_expat_features"])


if __name__ == "__main__":
    unittest.main()
