"""The Python JSON python-rapidjson path keeps its catalog, lock, oracle, receipts, and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/json"
PROJECT = ROOT / "projects/json/python/python-rapidjson"
OVERLAY = ROOT / "fuzzing/afl-native/json/python/python-rapidjson"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def parser_record() -> dict:
    parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "python-rapidjson"]
    return parser


class PythonJsonRapidjsonPilotTest(unittest.TestCase):
    def test_cell_counts_and_ranked_order(self):
        parsers = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")["leads"]
        cell = read(BASE / "cell.json")
        self.assertEqual([parser["name"] for parser in parsers][-1], "python-rapidjson")
        downloads = {lead["name"]: lead["last_month"] for lead in leads}
        metrics = [downloads[parser["name"]] for parser in parsers]
        self.assertEqual(metrics, sorted(metrics, reverse=True))
        self.assertEqual(len(parsers), cell["verified_third_party_count"])
        self.assertEqual(sum(lead["status"] == "lead" for lead in leads),
                         cell["unresolved_documentation_leads"])
        lead, = [lead for lead in leads if lead["name"] == "python-rapidjson"]
        self.assertEqual(lead["status"], "promoted_to_verified")
        parser = parser_record()
        self.assertEqual(parser["popularity"]["value"], lead["last_month"])
        self.assertEqual(parser["popularity"]["value"], 4066455)
        # Same Tencent RapidJSON family as the C++ path; not an independent parser.
        self.assertIn("RapidJSON", parser["family"])
        self.assertIn("projects/json/cpp/rapidjson", parser["family_note"])
        self.assertIn("not an independent parser", parser["family_note"])
        self.assertTrue((ROOT / "projects/json/cpp/rapidjson/manifest.json").is_file())
        self.assertIn("last value wins", parser["number_and_key_scope"])
        self.assertIn("python-rapidjson 1.26 (4,066,455)", cell["uncertainty"])
        ranking = (BASE / "ranking.md").read_text()
        self.assertIn("| 8 | [python-rapidjson]", ranking)

    def test_release_lock_matches_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")
        package = lock["python-rapidjson"]
        parser = parser_record()
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual(package["release"], manifest["release"])
        self.assertEqual(package["sdist_sha256"], manifest["source_sha256"])
        self.assertEqual(parser["source_sha256"], manifest["source_sha256"])
        self.assertEqual(parser["wheel_sha256"], package["wheel_sha256"])
        self.assertEqual(package["runtime_dependencies"], [])
        self.assertEqual(package["license"], parser["license"])
        self.assertEqual(lock["RapidJSON"]["license"], "MIT")
        for digest in (manifest["source_sha256"], package["rapidjson_cpp_sha256"],
                       package["license_file_sha256"], lock["RapidJSON"]["reader_h_sha256"],
                       lock["RapidJSON"]["license_file_sha256"]):
            self.assertIn(digest, dockerfile)
        self.assertIn(lock["RapidJSON"]["release"], dockerfile)
        self.assertTrue(lock["RapidJSON"]["git_commit"].startswith(lock["RapidJSON"]["release"][-8:]))
        requirements = (PROJECT / "build-requirements.lock").read_text()
        for name, entry in lock["build_backend"].items():
            if isinstance(entry, dict):
                self.assertIn(f"{name}=={entry['release']} --hash=sha256:{entry['wheel_sha256']}", requirements)
        self.assertIn("-fcoverage-mapping", dockerfile)
        self.assertIn(manifest["base_image"], dockerfile)

    def test_project_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser = parser_record()
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], parser["expected_output"])
        self.assertEqual(manifest["differential_expected_output"], parser["differential_expected_output"])
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        self.assertGreater(receipt["parser_source_lines_covered"], receipt["underlying_source_lines_covered"])
        for control, digest in ((manifest["control"], manifest["control_sha256"]),
                                (manifest["differential_control"], manifest["differential_control_sha256"])):
            self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        record, = [item for item in read(BASE / "verification.json")["third_party"]
                   if item["package"] == "python-rapidjson"]
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(record["output"], receipt["output"])
        self.assertEqual(record["native_region_start_lines"], receipt["parser_source_lines_covered"])
        self.assertEqual(record["rapidjson_region_start_lines"], receipt["underlying_source_lines_covered"])
        self.assertEqual(record["reader_h_lines"], receipt["format_specific_source_lines_covered"])
        self.assertEqual(record["wrapper_rapidjson_cpp_lines"],
                         receipt["parser_source_lines_covered"] - receipt["underlying_source_lines_covered"])

    def test_oracle_and_feedback_are_exact_stable_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / "python-rapidjson-valid-feedback.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        for oracle in (report["control_oracle"], report["variant_oracle"]):
            self.assertTrue(oracle["load_stream_matches_oracle"] and oracle["loads_bytes_matches_oracle"]
                            and oracle["loads_str_matches_oracle"])
            self.assertEqual(oracle["duplicate_keys"], 0)
            self.assertEqual(oracle["python_rapidjson"], manifest["release"])
            self.assertEqual(oracle["rapidjson_exact_version"], "v1.1.0-763-g24b5e7a8")
        self.assertNotEqual(report["control_oracle"]["tree_sha256"], report["variant_oracle"]["tree_sha256"])
        self.assertTrue(report["pass"] and report["control_repeat_identical"]
                        and report["variant_repeat_identical"])
        self.assertEqual(report["control_output"], manifest["expected_output"])
        self.assertEqual(report["variant_output"], manifest["differential_expected_output"])
        self.assertGreater(report["reader_h_feature_difference"], 0)
        self.assertGreater(report["afl_tuple_difference"], 0)
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(report["control_parser_features"],
                         report["control_rapidjson_features"] + report["control_wrapper_features"])


if __name__ == "__main__":
    unittest.main()
