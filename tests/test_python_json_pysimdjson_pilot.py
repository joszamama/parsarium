"""The Python JSON pysimdjson path keeps its catalog, lock, oracle, receipts, and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/json"
PROJECT = ROOT / "projects/json/python/pysimdjson"
OVERLAY = ROOT / "fuzzing/afl-native/json/python/pysimdjson"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PythonJsonPysimdjsonPilotTest(unittest.TestCase):
    def test_lead_is_promoted_with_its_saved_metric(self):
        leads = read(BASE / "leads.json")["leads"]
        lead, = [lead for lead in leads if lead["name"] == "pysimdjson"]
        self.assertEqual(lead["status"], "promoted_to_verified")
        parser, = [parser for parser in read(BASE / "parsers.json") if parser["name"] == "pysimdjson"]
        self.assertEqual(parser["popularity"]["value"], lead["last_month"])
        self.assertEqual(parser["popularity"]["value"], 679340)
        self.assertIn("simdjson 5.1.1", parser["family"])
        self.assertIn("5.0.4", parser["family_note"])
        cpp, = [item for item in read(ROOT / "data/cpp/json/parsers.json") if item["name"] == "simdjson"]
        self.assertEqual(cpp["version"], "5.0.4")

    def test_release_lock_matches_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "pysimdjson"]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual(lock["pysimdjson"]["release"], manifest["release"])
        self.assertEqual(lock["pysimdjson"]["sdist_sha256"], manifest["source_sha256"])
        self.assertEqual(parser["source_sha256"], manifest["source_sha256"])
        self.assertEqual(parser["wheel_sha256"], lock["pysimdjson"]["wheel_sha256"])
        self.assertEqual(lock["pysimdjson"]["runtime_dependencies"], [])
        self.assertEqual(lock["pysimdjson"]["license"], parser["license"])
        for digest in (manifest["source_sha256"], lock["pysimdjson"]["csimdjson_pyx_sha256"],
                       lock["pysimdjson"]["license_file_sha256"],
                       lock["simdjson"]["simdjson_cpp_sha256"], lock["simdjson"]["simdjson_h_sha256"]):
            self.assertIn(digest, dockerfile)
        requirements = (PROJECT / "build-requirements.lock").read_text()
        for name, entry in lock["build_backend"].items():
            if isinstance(entry, dict):
                self.assertIn(f"{name}=={entry['release']} --hash=sha256:{entry['wheel_sha256']}", requirements)
        self.assertIn("-fcoverage-mapping", dockerfile)

    def test_project_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "pysimdjson"]
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], parser["expected_output"])
        self.assertEqual(manifest["differential_expected_output"], parser["differential_expected_output"])
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        self.assertGreater(receipt["parser_source_lines_covered"], receipt["underlying_source_lines_covered"])
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        record, = [item for item in read(BASE / "verification.json")["third_party"]
                   if item["package"] == "pysimdjson"]
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(record["native_region_start_lines"], receipt["parser_source_lines_covered"])
        self.assertEqual(record["simdjson_region_start_lines"], receipt["underlying_source_lines_covered"])
        self.assertEqual(record["cython_wrapper_region_start_lines"] + record["simdjson_region_start_lines"],
                         receipt["parser_source_lines_covered"])

    def test_oracle_and_feedback_are_exact_stable_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / "pysimdjson-valid-feedback.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        for oracle in (report["control_oracle"], report["variant_oracle"]):
            self.assertTrue(oracle["parse_bytes_matches_oracle"] and oracle["load_path_matches_oracle"])
            self.assertTrue(oracle["stdlib_decoding_disabled"])
            self.assertEqual(oracle["duplicate_keys"], 0)
            self.assertEqual(oracle["simdjson"], "5.1.1")
            self.assertEqual(oracle["active_implementation"][0], "arm64")
        self.assertNotEqual(report["control_oracle"]["tree_sha256"], report["variant_oracle"]["tree_sha256"])
        self.assertTrue(report["pass"] and report["control_repeat_identical"]
                        and report["variant_repeat_identical"])
        self.assertEqual(report["control_output"], manifest["expected_output"])
        self.assertEqual(report["variant_output"], manifest["differential_expected_output"])
        self.assertGreater(report["simdjson_feature_difference"], 0)
        self.assertEqual(report["fallback_kernel_features"], 0)
        self.assertGreater(report["afl_tuple_difference"], 0)
        self.assertEqual(report["parser_feature_difference"],
                         report["simdjson_feature_difference"] + report["wrapper_feature_difference"])
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])


if __name__ == "__main__":
    unittest.main()
