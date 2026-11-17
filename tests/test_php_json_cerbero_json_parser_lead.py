"""cerbero/json-parser is a blocked lead: its own lazy parser path passes, parser feedback does not separate the controls."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/json"
PROBE = ROOT / "lead-probes/php/json/cerbero_json_parser"
CHECK = BASE / "cerbero-json-parser-lead-check.json"

_spec = importlib.util.spec_from_file_location("cerbero_lead_check", PROBE / "check.py")
check_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_module)


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return sha256(path.read_bytes()).hexdigest()


class PhpJsonCerberoJsonParserLeadTest(unittest.TestCase):
    def setUp(self):
        self.check = read(CHECK)

    def test_release_lock_archive_and_probe_files_are_pinned(self):
        locked, = read(PROBE / "composer.lock")["packages"]
        self.assertEqual((locked["name"], locked["version"], locked["source"]["reference"], locked["license"]),
                         (self.check["package"], self.check["release"], self.check["composer_reference"], ["MIT"]))
        self.assertEqual(self.check["composer_lock_sha256"], digest(PROBE / "composer.lock"))
        dockerfile = (PROBE / "Dockerfile").read_text()
        self.assertIn(self.check["archive_url"], dockerfile)
        self.assertIn(f"{self.check['archive_sha256']}  /work/parser-source.zip", dockerfile)
        self.assertIn("diff -r", dockerfile)
        for name, value in self.check["probe_file_sha256"].items():
            self.assertEqual(digest(PROBE / name), value, name)
        for name, value in self.check["bridge_file_sha256"].items():
            self.assertEqual(digest(ROOT / "fuzzing/afl-bridge" / name), value, name)
        self.assertEqual((PROBE / "afl_trace").read_bytes(),
                         (ROOT / "fuzzing/afl-native/json/php/pcrov_jsonreader/afl_trace").read_bytes())

    def test_metric_comes_from_the_php_registry_snapshot(self):
        popularity = self.check["popularity"]
        snapshot = read(BASE / "registry-snapshot.json")
        hits = {hit["downloads"] for query in snapshot["search"] for hit in query["hits"]
                if hit["name"] == self.check["package"]}
        self.assertEqual(hits, {popularity["value"]})
        self.assertEqual(popularity["captured_at_utc"], snapshot["captured_at_utc"])
        self.assertEqual(popularity["metric"], "Packagist total downloads")
        self.assertGreaterEqual(popularity["recheck"]["value"], popularity["value"])
        self.assertNotIn(self.check["package"], {item["name"] for item in read(BASE / "parsers.json")})

    def test_both_controls_match_independent_trees_through_all_sources(self):
        observed = {run["control"]: run for run in self.check["observed"]}
        self.assertEqual(set(observed), set(self.check["control_sha256"]))
        for name, value in self.check["control_sha256"].items():
            data = (ROOT / "controls/json" / name).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), value)
            self.assertEqual(observed[name]["tree"], check_module.oracle(data))
        self.assertEqual(observed["nested-object.json"]["tree"]["type"], "object")
        self.assertEqual(observed["nested-array.json"]["tree"]["type"], "array")
        self.assertTrue(self.check["type_tagged_trees_match_oracle"])
        self.assertTrue(self.check["file_and_stream_sources_match"])

    def test_lazy_mode_keeps_compounds_in_package_parser(self):
        for run in self.check["observed"]:
            decoder = run["decoder"]
            self.assertEqual(decoder["lazy_compound_inputs"], 0)
            self.assertTrue(decoder["lazy_tree_identical"])
            self.assertGreater(decoder["eager_compound_inputs"], 0)
        harness = (PROBE / "harness.php").read_text()
        code = re.sub(r"^\s*//.*$", "", harness, flags=re.M)
        self.assertIn("$parser->lazy()", code)
        self.assertIn("JsonParser::parse($input)", code)
        self.assertNotIn("json_decode", code)
        self.assertIn("ext/json", self.check["parser_family"])

    def test_feedback_is_blocked_with_measured_baseline(self):
        self.assertEqual(self.check["status"], "blocked_no_parser_feedback_differential")
        coverage = self.check["docker_source_coverage"]
        self.assertGreater(coverage["first_lines_covered"], 0)
        self.assertEqual(coverage["first_lines_covered"], coverage["second_lines_covered"])
        self.assertEqual(coverage["line_set_difference"], 0)
        afl = self.check["afl_feedback"]
        self.assertEqual(afl["subject_prefix"], "/work/vendor/cerbero/json-parser/")
        self.assertIn(f"ENV PARSARIUM_SUBJECT_PREFIX={afl['subject_prefix']}\n",
                      (PROBE / "Dockerfile.afl").read_text())
        self.assertTrue(afl["repeats_identical"])
        self.assertFalse(afl["mutation_campaign_run"])
        self.assertEqual((afl["parser_feature_difference"], afl["afl_tuple_difference"]), (0, 0))
        self.assertEqual(set(afl["no_parse_baseline_features"].values()), {0})
        self.assertGreater(afl["first_parser_features"], 0)
        self.assertGreater(afl["first_parser_only_tuples"], 0)
        self.assertLess(max(afl["no_parse_baseline_tuples"].values()), afl["first_afl_tuples"])
        calls = self.check["call_trace_observation"]
        self.assertEqual(calls["call_site_id_difference"], 0)
        self.assertGreater(calls["bucketed_call_site_difference"], 0)
        self.assertEqual(set(calls["no_parse_call_sites"].values()), {0})


if __name__ == "__main__":
    unittest.main()
