"""The Python JSON ujson path keeps its catalog, lock, oracle, receipts, and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/json"
PROJECT = ROOT / "projects/json/python/ujson"
OVERLAY = ROOT / "fuzzing/afl-native/json/python/ujson"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PythonJsonUjsonPilotTest(unittest.TestCase):
    def test_cell_counts_and_ranked_order(self):
        parsers = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")["leads"]
        cell = read(BASE / "cell.json")
        self.assertEqual([parser["name"] for parser in parsers],
                         ["pydantic", "jiter", "orjson", "json5", "simplejson", "ijson", "msgspec", "ujson",
                          "python-rapidjson", "pysimdjson"])
        downloads = {lead["name"]: lead["last_month"] for lead in leads}
        metrics = [downloads[parser["name"]] for parser in parsers]
        self.assertEqual(metrics, sorted(metrics, reverse=True))
        self.assertEqual(len(parsers), cell["verified_third_party_count"])
        self.assertEqual(sum(lead["status"] == "lead" for lead in leads),
                         cell["unresolved_documentation_leads"])
        lead, = [lead for lead in leads if lead["name"] == "ujson"]
        self.assertEqual(lead["status"], "promoted_to_verified")
        parser, = [parser for parser in parsers if parser["name"] == "ujson"]
        self.assertEqual(parser["popularity"]["value"], lead["last_month"])
        self.assertEqual(parser["popularity"]["value"], 29543889)
        self.assertIn("UltraJSON", parser["family"])
        self.assertIn("last value wins", parser["number_and_key_scope"])

    def test_release_lock_matches_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "ujson"]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual(lock["ujson"]["release"], manifest["release"])
        self.assertEqual(lock["ujson"]["sdist_sha256"], manifest["source_sha256"])
        self.assertEqual(parser["source_sha256"], manifest["source_sha256"])
        self.assertEqual(parser["wheel_sha256"], lock["ujson"]["wheel_sha256"])
        self.assertEqual(lock["ujson"]["runtime_dependencies"], [])
        self.assertEqual(lock["ujson"]["license"], parser["license"])
        for digest in (manifest["source_sha256"], lock["ujson"]["decode_c_sha256"],
                       lock["ujson"]["license_file_sha256"],
                       lock["double-conversion"]["string_to_double_cc_sha256"],
                       lock["double-conversion"]["strtod_cc_sha256"],
                       lock["double-conversion"]["license_file_sha256"]):
            self.assertIn(digest, dockerfile)
        requirements = (PROJECT / "build-requirements.lock").read_text()
        for name, entry in lock["build_backend"].items():
            if isinstance(entry, dict):
                self.assertIn(f"{name}=={entry['release']} --hash=sha256:{entry['wheel_sha256']}", requirements)
        self.assertIn("UJSON_BUILD_NO_STRIP=1", dockerfile)
        self.assertIn("-fcoverage-mapping", dockerfile)

    def test_project_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "ujson"]
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
                   if item["package"] == "ujson"]
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(record["output"], receipt["output"])
        self.assertEqual(record["native_region_start_lines"], receipt["parser_source_lines_covered"])

    def test_oracle_and_feedback_are_exact_stable_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / "ujson-valid-feedback.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        for oracle in (report["control_oracle"], report["variant_oracle"]):
            self.assertTrue(oracle["bytes_matches_oracle"] and oracle["str_matches_oracle"])
            self.assertEqual(oracle["duplicate_keys"], 0)
            self.assertEqual(oracle["ujson"], manifest["release"])
        self.assertNotEqual(report["control_oracle"]["tree_sha256"], report["variant_oracle"]["tree_sha256"])
        self.assertTrue(report["pass"] and report["control_repeat_identical"]
                        and report["variant_repeat_identical"])
        self.assertEqual(report["control_output"], manifest["expected_output"])
        self.assertEqual(report["variant_output"], manifest["differential_expected_output"])
        self.assertGreater(report["decode_c_feature_difference"], 0)
        self.assertGreater(report["double_conversion_feature_difference"], 0)
        self.assertGreater(report["afl_tuple_difference"], 0)
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])


if __name__ == "__main__":
    unittest.main()
