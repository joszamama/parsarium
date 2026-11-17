"""The Python JSON json5 path keeps its catalog, lock, search, oracle, receipts, and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/json"
PROJECT = ROOT / "projects/json/python/json5"
OVERLAY = ROOT / "fuzzing/afl-native/json/python/json5"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PythonJsonJson5PilotTest(unittest.TestCase):
    def test_cell_is_full_and_ranked_by_one_metric(self):
        parsers = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")["leads"]
        cell = read(BASE / "cell.json")
        snapshot = read(BASE / "registry-snapshot.json")
        self.assertEqual(len(parsers), cell["verified_third_party_count"])
        self.assertEqual(len(parsers), cell["ceiling"])
        downloads = {lead["name"]: lead["last_month"] for lead in leads}
        metrics = [downloads[parser["name"]] for parser in parsers]
        self.assertEqual(metrics, sorted(metrics, reverse=True))
        captured = {name: item["downloads"] for name, item in snapshot["download_metric"]["packages"].items()}
        for lead in leads:
            self.assertEqual(lead["last_month"], captured[lead["name"]], lead["name"])
        self.assertEqual(sum(lead["status"] == "lead" for lead in leads), cell["unresolved_documentation_leads"])
        self.assertEqual(sum(lead["status"] == "promoted_to_verified" for lead in leads), len(parsers))
        self.assertEqual({lead["name"] for lead in leads if lead["status"] == "promoted_to_verified"},
                         {parser["name"] for parser in parsers})
        lead, = [lead for lead in leads if lead["name"] == "json5"]
        parser, = [parser for parser in parsers if parser["name"] == "json5"]
        self.assertEqual(parser["popularity"]["value"], lead["last_month"])
        self.assertEqual(parser["popularity"]["value"], 50036028)
        self.assertIn("glop", parser["family"])

    def test_search_record_is_bounded_and_counted(self):
        cell = read(BASE / "cell.json")
        snapshot = read(BASE / "registry-snapshot.json")
        self.assertEqual(snapshot["search_limit_per_query"], cell["search_limit_per_query"])
        hits = [hit["name"] for search in snapshot["search"] for hit in search["hits"]]
        for search in snapshot["search"]:
            self.assertLessEqual(len(search["hits"]), search["limit"])
            self.assertEqual(len(search["hits"]), min(search["total"], search["limit"]))
        self.assertEqual(len(hits), cell["search_hits_recorded"])
        self.assertEqual(len(set(hits)), cell["unique_search_hits"])
        self.assertEqual(len(snapshot["search"]) + 1, len(cell["search_queries"]))
        self.assertIn("json5", [hit["name"] for search in snapshot["search"] for hit in search["hits"]])

    def test_release_lock_matches_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "json5"]
        release = read(BASE / "registry-snapshot.json")["releases"]["json5"]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        lock = (PROJECT / "runtime-requirements.lock").read_text()
        files = {item["filename"]: item["sha256"] for item in release["files"]}
        self.assertEqual(files["json5-0.17.3-py3-none-any.whl"], manifest["source_sha256"])
        self.assertEqual(files["json5-0.17.3.tar.gz"], manifest["sdist_sha256"])
        self.assertEqual(parser["wheel_sha256"], manifest["source_sha256"])
        self.assertEqual(parser["source_sha256"], manifest["sdist_sha256"])
        self.assertEqual(release["license_expression"], parser["license"])
        self.assertEqual(release["requires_dist"], [])
        self.assertEqual(lock.splitlines(), [
            f"json5==0.17.3 --hash=sha256:{manifest['source_sha256']}",
            f"atheris=={manifest['fuzz_engine_release']} --hash=sha256:{manifest['fuzz_engine_sha256']}"])
        for digest in (manifest["source_sha256"], manifest["sdist_sha256"], manifest["fuzz_engine_sha256"]):
            self.assertIn(digest, dockerfile)
        self.assertIn("diff -r /work/json5-sdist/json5 /work/json5-wheel/json5", dockerfile)

    def test_project_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "json5"]
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], parser["expected_output"])
        self.assertEqual(manifest["differential_expected_output"], parser["differential_expected_output"])
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        for control, digest in ((manifest["control"], manifest["control_sha256"]),
                                (manifest["differential_control"], manifest["differential_control_sha256"])):
            self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        record, = [item for item in read(BASE / "verification.json")["third_party"]
                   if item["package"] == "json5"]
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(record["output"], receipt["output"])
        self.assertEqual(record["parser_source_lines_covered"], receipt["parser_source_lines_covered"])

    def test_oracle_and_feedback_are_exact_stable_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / "json5-valid-feedback.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        for oracle in (report["control_oracle"], report["variant_oracle"]):
            self.assertTrue(oracle["bytes_matches_oracle"] and oracle["str_matches_oracle"]
                            and oracle["stream_matches_oracle"])
            self.assertEqual(oracle["duplicate_keys"], 0)
            self.assertEqual(oracle["json5"], manifest["release"])
        self.assertNotEqual(report["control_oracle"]["tree_sha256"], report["variant_oracle"]["tree_sha256"])
        self.assertTrue(report["pass"] and report["control_repeat_identical"]
                        and report["variant_repeat_identical"])
        self.assertGreaterEqual(report["runs_per_control"], 2)
        self.assertEqual(report["control_output"], manifest["expected_output"])
        self.assertEqual(report["variant_output"], manifest["differential_expected_output"])
        self.assertGreater(report["parser_py_feature_difference"], 0)
        self.assertGreater(report["afl_tuple_difference"], 0)
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(report["control_afl_tuples"], overlay["feedback_edges"])


if __name__ == "__main__":
    unittest.main()
