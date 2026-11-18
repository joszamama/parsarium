import importlib.util
import json
from hashlib import sha256
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data/go/yaml"
_spec = importlib.util.spec_from_file_location("yaml_check_controls", ROOT / "controls/yaml/check_controls.py")
controls = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(controls)


def read(path: Path):
    return json.loads(path.read_text())


class GoYamlPilotTest(unittest.TestCase):
    def setUp(self):
        self.parsers = read(CELL / "parsers.json")
        self.cell = read(CELL / "cell.json")
        self.feedback = {item["project"]: item for item in read(CELL / "afl-feedback.json")["results"]}

    def test_cell_counts_match_parser_rows(self):
        self.assertEqual(self.cell["verified_third_party_count"], len(self.parsers))
        self.assertEqual(self.cell["verified_standard_or_runtime_count"], 0)
        values = [row["popularity"]["value"] for row in self.parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        leads = {lead["name"]: lead for lead in read(CELL / "leads.json")}
        for row in self.parsers:
            self.assertEqual(leads[row["name"]]["status"], "selected")
            self.assertEqual(leads[row["name"]]["metric_value"], row["popularity"]["value"])

    def test_rows_match_oracle_and_receipts(self):
        for row in self.parsers:
            with self.subTest(row=row["name"]):
                project = ROOT / row["project"]
                manifest = read(project / "manifest.json")
                self.assertEqual(row["expected_output"], {"tree": controls.EXPECTED["catalog.yaml"]})
                self.assertEqual(row["differential_expected_output"], {"tree": controls.EXPECTED["order.yaml"]})
                self.assertEqual(manifest["expected_output"], row["expected_output"])
                self.assertEqual(manifest["release"], row["version"])
                receipt = read(project / "verification.json")
                self.assertTrue(receipt["pass"])
                self.assertEqual(receipt["output"], row["expected_output"])
                self.assertGreater(receipt["parser_source_lines_covered"], 0)
                self.assertEqual(manifest["control_sha256"],
                                 sha256((ROOT / manifest["control"]).read_bytes()).hexdigest())
                lock = read(project / "source-lock.json")[row["name"]]
                self.assertEqual(lock.get("go_module", row["name"]), row["module"])
                self.assertEqual(lock["source_sha256"], manifest["source_sha256"])
                self.assertIn(manifest["source_sha256"], (project / "Dockerfile").read_text())
                self.assertIn(f"{row['module']} {row['version']} {lock['go_module_sum']}",
                              (project / "go.sum").read_text())

    def test_afl_feedback_is_stable_and_input_dependent(self):
        for row in self.parsers:
            with self.subTest(row=row["name"]):
                slug = row["project"].rsplit("/", 1)[1]
                result = self.feedback[f"yaml/go/{slug}"]
                overlay = ROOT / "fuzzing/afl-native/yaml/go" / slug / "verification.json"
                self.assertEqual(result["overlay_receipt_sha256"], sha256(overlay.read_bytes()).hexdigest())
                self.assertEqual(result["runs_per_control"], 3)
                self.assertTrue(result["repeated_control_identical"] and result["repeated_differential_identical"])
                self.assertGreater(result["parser_feature_difference"], 0)
                self.assertGreater(result["afl_tuple_difference"], 0)
                self.assertTrue(set(result["difference_features_by_file"]) &
                                {"scannerc.go", "parserc.go", "scanner.go", "parser.go"})

    def test_v2_harness_keeps_mapping_order(self):
        if not any(row["name"] == "gopkg.in/yaml.v2" for row in self.parsers):
            self.skipTest("yaml.v2 not selected")
        harness = (ROOT / "projects/yaml/go/gopkg_in_yaml_v2/harness.go").read_text()
        self.assertIn("yaml.MapSlice", harness)
        self.assertIn("UnmarshalYAML", harness)

    def test_goccy_harness_keeps_mapping_order(self):
        if not any(row["name"] == "github.com/goccy/go-yaml" for row in self.parsers):
            self.skipTest("goccy/go-yaml not selected")
        harness = (ROOT / "projects/yaml/go/github_com_goccy_go_yaml/harness.go").read_text()
        self.assertIn("yaml.UseOrderedMap()", harness)
        self.assertIn("case yaml.MapSlice:", harness)
        self.assertNotIn("gopkg.in/yaml", harness)

    def test_unselected_leads_have_recorded_evidence(self):
        leads = read(CELL / "leads.json")
        check = read(CELL / "lead-check.json")
        for lead in leads:
            with self.subTest(lead=lead["name"]):
                self.assertTrue(lead["reason"])
                if lead.get("evidence"):
                    self.assertTrue((ROOT / lead["evidence"]).is_file())
        probes = check["leads"]
        for name in ("ghodss", "sigs", "apimachinery", "koanf", "gypsy"):
            self.assertFalse(probes[name]["oracle_match_both"])
        for name in ("kyaml", "cue"):
            self.assertTrue(probes[name]["oracle_match_both"])
            self.assertGreater(probes[name]["source_block_feedback"]["underlying_go_yaml_in_v3"]["block_difference"], 0)
        self.assertEqual(probes["kyaml"]["source_block_feedback"]["own"]["block_difference"], 0)
        overlap = {(row["module"], row["version"]): row for row in check["source_overlap"]}
        renamed = overlap[("go.yaml.in/yaml/v3", "v3.0.6")]
        self.assertGreater(renamed["shared_distinct_lines"] / renamed["distinct_non_test_lines"], 0.99)
        v4 = overlap[("go.yaml.in/yaml/v4", "v4.0.0")]
        self.assertLess(v4["shared_distinct_lines"] / v4["distinct_non_test_lines"], 0.5)

    def test_v4_harness_uses_v4_load_api(self):
        if not any(row["name"] == "go.yaml.in/yaml/v4" for row in self.parsers):
            self.skipTest("go.yaml.in/yaml/v4 not selected")
        harness = (ROOT / "projects/yaml/go/go_yaml_in_yaml_v4/harness.go").read_text()
        self.assertIn('"go.yaml.in/yaml/v4"', harness)
        self.assertIn("yaml.Load(data, &document)", harness)
        self.assertNotIn("yaml.Unmarshal(", harness)
        manifest = read(ROOT / "projects/yaml/go/go_yaml_in_yaml_v4/manifest.json")
        self.assertEqual(manifest["coverage_subject_prefix"], "go.yaml.in/yaml/v4/")

    def test_go_rotini_harness_keeps_mapping_order(self):
        if not any(row["name"] == "github.com/go-rotini/yaml" for row in self.parsers):
            self.skipTest("go-rotini/yaml not selected")
        project = ROOT / "projects/yaml/go/github_com_go_rotini_yaml"
        harness = (project / "harness.go").read_text()
        self.assertIn('"github.com/go-rotini/yaml"', harness)
        self.assertIn("yaml.WithOrderedMap()", harness)
        self.assertIn("case yaml.MapSlice:", harness)
        self.assertNotIn("goccy", harness)
        self.assertIn("-coverpkg=github.com/go-rotini/yaml/...", (project / "Dockerfile").read_text())
        manifest = read(project / "manifest.json")
        self.assertEqual(manifest["coverage_subject_prefix"], "github.com/go-rotini/yaml/")
        row = next(row for row in self.parsers if row["name"] == "github.com/go-rotini/yaml")
        self.assertEqual(row["popularity"]["value"], 2)
        self.assertIn("independent", row["family"])

    def test_golib_harness_parses_then_evaluates_core_schema(self):
        name = "github.com/yongjohnlee80/golib/parse/yaml"
        if not any(row["name"] == name for row in self.parsers):
            self.skipTest("golib parse/yaml not selected")
        project = ROOT / "projects/yaml/go/github_com_yongjohnlee80_golib_parse_yaml"
        harness = (project / "harness.go").read_text()
        self.assertIn('pyaml "github.com/yongjohnlee80/golib/parse/yaml"', harness)
        self.assertIn("pyaml.Parse(data)", harness)
        self.assertIn("yaml.Evaluate(stream.Docs[0], yaml.Core)", harness)
        self.assertIn("case yaml.Map:", harness)
        # Coverage and AFL++ feedback stay inside the parser and its same-module schema evaluator.
        dockerfile = (project / "Dockerfile").read_text()
        self.assertIn("-coverpkg=github.com/yongjohnlee80/golib/parse/yaml,github.com/yongjohnlee80/golib/yaml ",
                      dockerfile)
        manifest = read(project / "manifest.json")
        self.assertEqual(manifest["coverage_subject_prefix"], "github.com/yongjohnlee80/golib/")
        row = next(row for row in self.parsers if row["name"] == name)
        self.assertEqual(row["module"], "github.com/yongjohnlee80/golib")
        coverage = read(project / "verification.json")
        self.assertEqual(coverage["parser_source_files"], 8)
        feedback = self.feedback["yaml/go/github_com_yongjohnlee80_golib_parse_yaml"]
        self.assertLessEqual(set(feedback["control_features_by_file"]),
                             {"compose.go", "encoding.go", "parser.go", "scanner.go", "yaml.go",
                              "evaluate.go", "resolve.go"})
        # Ties go-rotini/yaml at 2 Imported by; the tie is ordered by package path.
        names = [row["name"] for row in self.parsers]
        self.assertLess(names.index("github.com/go-rotini/yaml"), names.index(name))

    def test_tabnas_harness_keeps_order_and_types_float64_numbers(self):
        name = "github.com/tabnas/yaml/go"
        if not any(row["name"] == name for row in self.parsers):
            self.skipTest("tabnas/yaml not selected")
        project = ROOT / "projects/yaml/go/github_com_tabnas_yaml_go"
        harness = (project / "harness.go").read_text()
        self.assertIn('tabnasyaml "github.com/tabnas/yaml/go"', harness)
        self.assertIn("tabnasyaml.Parse(string(data))", harness)
        self.assertIn("case *tabnas.OrderedMap:", harness)
        self.assertIn("range node.Keys", harness)
        # Every number is float64; only finite integral values become int, and no control holds an integral float.
        self.assertIn("node == math.Trunc(node)", harness)
        self.assertNotIn("goccy", harness)
        # Coverage and AFL++ feedback cover the plugin and the three tabnas modules it parses with, all pinned.
        dockerfile = (project / "Dockerfile").read_text()
        self.assertIn("-coverpkg=github.com/tabnas/yaml/go,github.com/tabnas/jsonic/go,"
                      "github.com/tabnas/parser/go,github.com/tabnas/json/go ", dockerfile)
        lock = read(project / "source-lock.json")
        go_sum = (project / "go.sum").read_text()
        for module, pin in lock.items():
            with self.subTest(module=module):
                self.assertIn(pin["source_sha256"], dockerfile)
                self.assertIn(f"{module} {pin['release']} {pin['go_module_sum']}", go_sum)
                self.assertEqual(pin["license"], "MIT")
        self.assertEqual(read(project / "manifest.json")["coverage_subject_prefix"], "github.com/tabnas/")
        feedback = self.feedback["yaml/go/github_com_tabnas_yaml_go"]
        self.assertIn("yaml.go", feedback["difference_features_by_file"])
        row = next(row for row in self.parsers if row["name"] == name)
        self.assertEqual(row["popularity"]["value"], 3)
        self.assertIn("jsonic", row["family"])
        names = [row["name"] for row in self.parsers]
        self.assertLess(names.index(name), names.index("github.com/go-rotini/yaml"))

    def test_round_four_leads_are_decided(self):
        leads = {lead["name"]: lead for lead in read(CELL / "leads.json")}
        check = read(CELL / "round4-lead-check.json")
        self.assertEqual(self.cell["leads_recorded"], len(leads))
        # Paths promoted in later rounds rank below every round-4 lead; compare with the round-4 selection.
        lowest = min(row["popularity"]["value"] for row in self.parsers
                     if not leads[row["name"]]["found_by"].endswith(("_round_6", "_round_7")))
        for name, metric in check["metrics"].items():
            with self.subTest(lead=name):
                lead = leads[name]
                self.assertNotEqual(lead["status"], "selected")
                self.assertEqual(lead["metric_value"], metric["value"])
                self.assertEqual(lead["evidence"], "data/go/yaml/round4-lead-check.json")
        above = [name for name in check["metrics"] if leads[name]["metric_value"] > lowest]
        self.assertEqual(sorted(above), ["github.com/beego/goyaml2", "gopkg.in/yaml.v1"])
        for row in check["source_overlap"]:
            self.assertGreater(row["shared_distinct_lines"] / row["distinct_non_test_lines"], 0.9)
        for probe in check["probes"].values():
            self.assertFalse(any(result["oracle_match"] for result in probe["controls"].values()))
        for name, metric in check["zero_metric_hits_not_leads"].items():
            self.assertEqual(metric["value"], 0)
            self.assertNotIn(name, leads)

    def test_round_six_leads_are_decided(self):
        leads = {lead["name"]: lead for lead in read(CELL / "leads.json")}
        check = read(CELL / "round6-lead-check.json")
        self.assertEqual(self.cell["leads_recorded"], len(leads))
        self.assertEqual({s["query"] for s in check["searches"]},
                         {"yaml parser", "yaml decoder", "yaml 1.2", "yaml lexer", "yaml ast", "yaml unmarshal"})
        for search in check["searches"]:
            self.assertEqual(search["hits_recorded"], len(search["hits"]))
            self.assertLessEqual(len(search["hits"]), 100)
        selected = {row["name"]: row for row in self.parsers}
        for name, metric in check["selected"].items():
            with self.subTest(selected=name):
                self.assertEqual(leads[name]["status"], "selected")
                self.assertEqual(selected[name]["popularity"]["value"], metric["value"])
                self.assertEqual(selected[name]["project"], metric["project"])
        for name, metric in check["metrics"].items():
            with self.subTest(lead=name):
                lead = leads[name]
                self.assertNotEqual(lead["status"], "selected")
                self.assertEqual(lead["metric_value"], metric["value"])
                self.assertEqual(lead["evidence"], "data/go/yaml/round6-lead-check.json")
                self.assertTrue(lead["reason"])
        # Every new hit with a positive value is decided: selected, a lead, or a subpackage of a selected module.
        hits = {hit["name"]: hit["imported_by"] for search in check["searches"] for hit in search["hits"]}
        decided = set(check["selected"]) | set(check["metrics"]) | set(check["not_separate"])
        for name in decided:
            self.assertGreater(hits[name], 0)
        self.assertEqual(len(decided), check["hit_counts"]["new_positive_metric"])
        for name in check["zero_metric_hits_not_leads"]:
            self.assertEqual(hits[name], 0)
            self.assertNotIn(name, leads)
        for row in check["source_overlap"]:
            with self.subTest(fork=row["module"]):
                self.assertGreater(row["shared_distinct_lines"] / row["distinct_non_test_lines"], 0.85)
                self.assertEqual(leads[row.get("package", row["module"])]["status"], "excluded_duplicate_fork")
        reference = check["probes"]["github.com/yamlstar/yamlstar-plugin-parser-reference/parser"]
        self.assertFalse(reference["controls"]["catalog.yaml"]["oracle_match"])
        self.assertEqual(leads["github.com/yamlstar/yamlstar-plugin-parser-reference/parser"]["status"],
                         "excluded_control_failed")

    def test_round_seven_leads_are_decided(self):
        leads = {lead["name"]: lead for lead in read(CELL / "leads.json")}
        check = read(CELL / "round7-lead-check.json")
        self.assertEqual(self.cell["leads_recorded"], len(leads))
        # pkg.go.dev cannot page past 100 hits: page 2 repeats the window and limit=200 returns nothing.
        for paging in check["paging_check"]:
            with self.subTest(paging=paging["query"]):
                self.assertEqual(paging["limit200_hits"], 0)
                self.assertLessEqual(len(paging["page2_not_in_page1"]), 2)
        self.assertEqual({s["query"] for s in check["searches"] if s["mode"] == "package"},
                         {"yml", "yaml tokenizer", "yaml node", "yaml document", "yaml stream", "yaml event",
                          "libyaml go", "libyaml", "yaml scanner", "yaml reader", "yaml loader", "yaml library"})
        self.assertEqual({s["query"] for s in check["searches"] if s["mode"] == "symbol"},
                         {"yaml Unmarshal", "yaml Parse", "yaml Decoder", "yaml Node", "yaml Load", "yaml Event",
                          "yaml Token", "yaml Scanner"})
        for search in check["searches"]:
            self.assertEqual(search["hits_recorded"], len(search["hits"]))
            self.assertLessEqual(len(search["hits"]), 100)
        selected = {row["name"]: row for row in self.parsers}
        for name, metric in check["selected"].items():
            with self.subTest(selected=name):
                self.assertEqual(leads[name]["status"], "selected")
                self.assertEqual(leads[name]["found_by"], "registry_search_round_7")
                self.assertEqual(selected[name]["popularity"]["value"], metric["value"])
                self.assertEqual(selected[name]["project"], metric["project"])
                self.assertTrue(all(result["oracle_match"] for result in check["probes"][name]["controls"].values()))
        for name, metric in check["metrics"].items():
            with self.subTest(lead=name):
                lead = leads[name]
                self.assertNotEqual(lead["status"], "selected")
                self.assertEqual(lead["metric_value"], metric["value"])
                self.assertEqual(lead["evidence"], "data/go/yaml/round7-lead-check.json")
                self.assertTrue(lead["reason"])
        hits = {}
        for search in check["searches"]:
            for hit in search["hits"]:
                hits[hit["name"]] = max(hits.get(hit["name"], 0), hit["imported_by"] or 0)
        decided = set(check["selected"]) | set(check["metrics"]) | set(check["not_separate"])
        for name in decided:
            self.assertGreater(hits[name], 0)
        self.assertEqual(len(decided), check["hit_counts"]["new_positive_metric"])
        for name in check["zero_metric_hits_not_leads"]:
            self.assertEqual(hits[name], 0)
            self.assertNotIn(name, leads)
        for row in check["source_overlap"]:
            with self.subTest(fork=row["package"]):
                self.assertGreater(row["shared_distinct_lines"] / row["distinct_non_test_lines"], 0.85)
                self.assertEqual(leads[row["package"]]["status"], "excluded_duplicate_fork")
        ytt, = check["normalized_overlap"]
        self.assertGreater(ytt["normalized_share"], 0.85)
        self.assertEqual(leads["carvel.dev/ytt/pkg/yamlmeta"]["status"], "excluded")


if __name__ == "__main__":
    unittest.main()
