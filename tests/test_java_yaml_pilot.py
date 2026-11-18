"""Static checks for the Java YAML pilot paths (no Docker)."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/java/yaml"
_spec = importlib.util.spec_from_file_location("yaml_check_controls", ROOT / "controls/yaml/check_controls.py")
oracle = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(oracle)


def read(path: Path):
    return json.loads(path.read_text())


class JavaYamlPilotTest(unittest.TestCase):
    def setUp(self):
        self.parsers = read(DATA / "parsers.json")
        self.cell = read(DATA / "cell.json")
        self.feedback = {row["project"]: row for row in read(DATA / "afl-feedback.json")["results"]}

    def test_cell_counts_selected_paths(self):
        self.assertGreaterEqual(len(self.parsers), 1)
        self.assertEqual(self.cell["verified_third_party_count"], len(self.parsers))
        self.assertEqual(self.cell["verified_standard_or_runtime_count"], 0)
        selected = {lead["name"] for lead in read(DATA / "leads.json") if lead["status"] == "selected"}
        self.assertEqual(selected, {f"{parser['group']}:{parser['artifact']}" for parser in self.parsers})
        values = [parser["popularity"]["value"] for parser in self.parsers]
        self.assertEqual(values, sorted(values, reverse=True))

    def test_trees_match_hand_written_oracle(self):
        for parser in self.parsers:
            with self.subTest(parser=parser["name"]):
                self.assertEqual(parser["expected_output"], {"tree": oracle.EXPECTED["catalog.yaml"]})
                self.assertEqual(parser["differential_expected_output"], {"tree": oracle.EXPECTED["order.yaml"]})
                receipt = read(ROOT / parser["project"] / "verification.json")
                self.assertTrue(receipt["pass"])
                self.assertEqual(receipt["output"], parser["expected_output"])
                self.assertGreater(receipt["parser_source_lines_covered"], 0)

    def test_pinned_release_and_documented_api(self):
        for parser in self.parsers:
            with self.subTest(parser=parser["name"]):
                manifest = read(ROOT / parser["project"] / "manifest.json")
                lock = read(ROOT / manifest["source_lock"])[parser["name"]]
                dockerfile = (ROOT / parser["project"] / "Dockerfile").read_text()
                self.assertEqual(lock["release"], parser["version"])
                for digest in (lock["jar_sha256"], lock["source_sha256"], lock["pom_sha256"]):
                    self.assertIn(digest, dockerfile)
                self.assertEqual(lock["license"], parser["license"])
                self.assertIn(parser["license"], {"Apache-2.0", "MIT"})
                self.assertTrue(parser["documentation"].startswith(("https://javadoc.io/static/", "https://github.com/")))
                self.assertIsInstance(parser["popularity"]["value"], int)
                self.assertEqual(manifest["control_sha256"],
                                 sha256((ROOT / "controls/yaml/catalog.yaml").read_bytes()).hexdigest())

    def test_afl_feedback_is_stable_and_input_dependent(self):
        for parser in self.parsers:
            project = parser["project"].removeprefix("projects/")
            with self.subTest(project=project):
                row = self.feedback[project]
                overlay = read(ROOT / "fuzzing/afl-native" / project / "verification.json")
                self.assertTrue(row["pass"] and overlay["pass"])
                self.assertEqual(row["runs_per_control"], 3)
                self.assertTrue(row["control_repeat_identical"] and row["differential_repeat_identical"])
                self.assertGreater(row["parser_feature_difference"], 0)
                self.assertGreater(row["afl_tuple_difference"], 0)
                self.assertEqual(overlay["base_project_receipt_sha256"],
                                 sha256((ROOT / parser["project"] / "verification.json").read_bytes()).hexdigest())
                self.assertEqual(row["control_parser_features"], overlay["parser_source_features"])

    def test_wrapper_paths_report_underlying_parser_feedback(self):
        for parser in self.parsers:
            manifest = read(ROOT / parser["project"] / "manifest.json")
            if "underlying_coverage_subject_prefix" not in manifest:
                continue
            project = parser["project"].removeprefix("projects/")
            with self.subTest(project=project):
                self.assertIn("wrapper", parser["family"].lower() + parser["family_note"].lower())
                receipt = read(ROOT / parser["project"] / "verification.json")
                self.assertGreater(receipt["underlying_source_lines_covered"], 0)
                self.assertTrue(manifest["afl_underlying_jar"] and manifest["afl_underlying_sources"])
                row = self.feedback[project]
                self.assertGreater(row["core_feature_difference"], 0)
                self.assertEqual(row["wrapper_control_features"] + row["core_control_features"],
                                 row["control_parser_features"])

    def test_zio_json_yaml_wraps_the_selected_snakeyaml_release(self):
        zio = read(ROOT / "projects/yaml/java/zio_json_yaml/source-lock.json")["zio-json-yaml"]
        snakeyaml = read(ROOT / "projects/yaml/java/snakeyaml/source-lock.json")["snakeyaml"]
        self.assertEqual(zio["underlying"]["coordinate"], "org.yaml:snakeyaml:2.7")
        self.assertEqual(zio["underlying"]["jar_sha256"], snakeyaml["jar_sha256"])
        self.assertEqual(zio["underlying"]["source_sha256"], snakeyaml["source_sha256"])
        row = self.feedback["yaml/java/zio_json_yaml"]
        self.assertEqual(row["wrapper_feature_difference"], 0)
        self.assertEqual(row["core_feature_difference"], row["parser_feature_difference"])

    def test_jackson_alias_failure_stays_a_lead(self):
        lead, = [lead for lead in read(DATA / "leads.json")
                 if lead["name"] == "com.fasterxml.jackson.dataformat:jackson-dataformat-yaml"]
        self.assertEqual(lead["status"], "fails_control")
        self.assertIn("anchor name", lead["reason"])

    def test_round_two_lead_decisions_have_evidence(self):
        leads = read(DATA / "leads.json")
        snapshot = read(DATA / "registry-snapshot.json")
        cell = read(DATA / "cell.json")
        self.assertEqual(cell["leads_recorded"], len(leads))
        self.assertEqual(sum(cell["leads_by_status"].values()), len(leads))
        lowest = min(parser["popularity"]["value"] for parser in self.parsers)
        for lead in leads:
            with self.subTest(lead=lead["name"]):
                self.assertIn(lead["name"], snapshot["metrics"])
                self.assertEqual(lead["metric_value"], snapshot["metrics"][lead["name"]]["value"])
                if lead["status"] != "selected":
                    self.assertIn(lead["status"], {"fails_control", "excluded", "unresolved"})
                    self.assertTrue(lead["reason"] and lead["evidence"])
        # Every lead ranked above the lowest selected path was decided, not left unresolved.
        self.assertFalse([lead["name"] for lead in leads
                          if lead["status"] == "unresolved" and (lead["metric_value"] or 0) > lowest])
        decisions = {lead["name"]: lead["status"] for lead in leads}
        self.assertEqual(decisions["tools.jackson.dataformat:jackson-dataformat-yaml"], "fails_control")
        self.assertEqual(decisions["com.charleskorn.kaml:kaml-jvm"], "fails_control")
        self.assertEqual(decisions["org.wso2.orbit.org.yaml:snakeyaml"], "excluded")

    def test_round_three_closes_every_recorded_lead(self):
        leads = read(DATA / "leads.json")
        snapshot = read(DATA / "registry-snapshot.json")
        decisions = {lead["name"]: lead for lead in leads}
        # The cell stays below ten only because no positive-metric lead is left undecided.
        self.assertFalse([name for name, lead in decisions.items() if lead["status"] == "unresolved"])
        self.assertLess(self.cell["verified_third_party_count"], 10)
        for name in ("io.circe:circe-yaml-v12_2.13", "dev.dejvokep:boosted-yaml", "net.jcazevedo:moultingyaml_2.12",
                     "io.maryk:maryk-yaml-jvm", "org.apache.commons:commons-configuration2"):
            self.assertEqual(decisions[name]["status"], "fails_control", name)
        for name in ("org.springframework:spring-beans", "dev.zio:zio-json-yaml_2.12", "dev.zio:zio-json-yaml_3",
                     "org.treblereel.gwt.yaml:eo-yaml", "org.noear:solon.config.yaml"):
            self.assertEqual(decisions[name]["status"], "excluded", name)
        self.assertIn("70%", decisions["io.circe:circe-yaml-v12_2.13"]["reason"])
        round3 = snapshot["round_3_targeted_leads"]
        for name in round3["leads_added"]:
            self.assertIn(name, decisions)
        for name, metric in round3["zero_metric_hits_not_leads"].items():
            self.assertEqual(metric["value"], 0, name)
            self.assertNotIn(name, decisions)

    def test_round_four_discovery_routes_are_decided(self):
        leads = read(DATA / "leads.json")
        snapshot = read(DATA / "registry-snapshot.json")
        decisions = {lead["name"]: lead for lead in leads}
        round4 = snapshot["round_4_targeted_leads"]
        for name in round4["leads_added"]:
            self.assertIn(name, decisions)
            self.assertIn(decisions[name]["status"], {"fails_control", "excluded"}, name)
            self.assertTrue(decisions[name]["note"].startswith("Discovery route: round 4"), name)
        for name in ("org.apache.groovy:groovy-yaml", "org.openrewrite:rewrite-yaml", "org.jruby:yecht",
                     "dev.hnaderi:yaml4s-snake_2.13", "org.jruby.extras:jvyamlb"):
            self.assertEqual(decisions[name]["status"], "fails_control", name)
        for name, metric in round4["zero_metric_hits_not_leads"].items():
            self.assertEqual(metric["value"], 0, name)
            self.assertNotIn(name, decisions)
        self.assertIn("Round 4", self.cell["uncertainty"])


if __name__ == "__main__":
    unittest.main()
