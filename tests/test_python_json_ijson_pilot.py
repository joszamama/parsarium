"""The Python JSON ijson path keeps its catalog, lock, receipts, and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/json"
PROJECT = ROOT / "projects/json/python/ijson"
OVERLAY = ROOT / "fuzzing/afl-native/json/python/ijson"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PythonJsonIjsonPilotTest(unittest.TestCase):
    def test_cell_counts_and_ranked_order(self):
        parsers = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")["leads"]
        cell = read(BASE / "cell.json")
        self.assertEqual([parser["name"] for parser in parsers],
                         ["pydantic", "orjson", "simplejson", "ijson", "msgspec", "ujson"])
        downloads = {lead["name"]: lead["last_month"] for lead in leads}
        metrics = [downloads[parser["name"]] for parser in parsers]
        self.assertEqual(metrics, sorted(metrics, reverse=True))
        self.assertEqual(len(parsers), cell["verified_third_party_count"])
        self.assertEqual(sum(lead["status"] == "lead" for lead in leads),
                         cell["unresolved_documentation_leads"])
        ijson_lead, = [lead for lead in leads if lead["name"] == "ijson"]
        self.assertEqual(ijson_lead["status"], "promoted_to_verified")
        ijson, = [parser for parser in parsers if parser["name"] == "ijson"]
        self.assertEqual(ijson["popularity"]["value"], ijson_lead["last_month"])
        self.assertIn("yajl2_c", ijson["family"])

    def test_release_lock_matches_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "ijson"]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual(lock["ijson"]["release"], manifest["release"])
        self.assertEqual(lock["ijson"]["sdist_sha256"], manifest["source_sha256"])
        self.assertEqual(parser["source_sha256"], manifest["source_sha256"])
        self.assertEqual(parser["wheel_sha256"], lock["ijson"]["wheel_sha256"])
        self.assertEqual(lock["ijson"]["runtime_dependencies"], [])
        self.assertEqual(lock["ijson"]["license"], parser["license"])
        for digest in (manifest["source_sha256"], lock["yajl"]["archive_sha256"],
                       lock["yajl"]["yajl_parser_c_sha256"], lock["yajl"]["yajl_lex_c_sha256"],
                       lock["yajl"]["commit"]):
            self.assertIn(digest, dockerfile)
        self.assertIn(lock["setuptools"]["wheel_sha256"],
                      (PROJECT / "build-requirements.lock").read_text())
        self.assertIn("IJSON_EMBED_YAJL=1", dockerfile)
        self.assertIn("ijson.backend_name != 'yajl2_c'", (PROJECT / "harness.py").read_text())

    def test_project_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "ijson"]
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
                   if item["package"] == "ijson"]
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(record["output"], receipt["output"])

    def test_feedback_is_stable_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / "ijson-valid-feedback.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["tested_backend"], "yajl2_c")
        self.assertTrue(report["pass"] and report["control_repeat_identical"]
                        and report["variant_repeat_identical"])
        self.assertEqual(report["control_output"], manifest["expected_output"])
        self.assertEqual(report["variant_output"], manifest["differential_expected_output"])
        self.assertGreater(report["parser_feature_difference"], 0)
        self.assertGreater(report["yajl_feature_difference"], 0)
        self.assertGreater(report["afl_tuple_difference"], 0)
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])


if __name__ == "__main__":
    unittest.main()
