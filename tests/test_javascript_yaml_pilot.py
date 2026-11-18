"""JavaScript YAML pilot paths match the hand-written typed-tree oracle and pinned feedback."""

from hashlib import sha256
import json
from pathlib import Path
import runpy
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/javascript/yaml"
ORACLE = runpy.run_path(str(ROOT / "controls/yaml/check_controls.py"))
CONTROL_NAMES = {"controls/yaml/catalog.yaml": "catalog.yaml", "controls/yaml/order.yaml": "order.yaml"}
SLUGS = {"js-yaml": "js_yaml", "yaml": "yaml", "yaml-ast-parser": "yaml_ast_parser",
         "@stoplight/yaml": "stoplight_yaml", "yaml-eslint-parser": "yaml_eslint_parser",
         "yaml-js": "yaml_js", "@visulima/yaml": "visulima_yaml", "@amritk/yaml": "amritk_yaml",
         "yaml-to-momoa": "yaml_to_momoa", "yaml.min": "yaml_min"}
# Upstream tag in each pinned documentation URL.
DOC_TAGS = {"js-yaml": "5.5.0", "yaml": "v2.9.1", "yaml-ast-parser": "0.0.43", "@stoplight/yaml": "v4.3.0",
            "yaml-eslint-parser": "v2.1.0", "yaml-js": "0.3.1",
            "@visulima/yaml": "%40visulima/yaml%402.0.0", "@amritk/yaml": "%40amritk/yaml%400.8.1",
            "yaml-to-momoa": "0fe4b94a79f198a90d2fdbd47e718e0275428826", "yaml.min": "v2.0.0"}
# Documented text API each adapter calls.
API_CALLS = {"js-yaml": "jsyaml.load(text)", "yaml": "YAML.parseDocument(text)", "yaml-ast-parser": "yaml.load(text)",
             "@stoplight/yaml": "yaml.parseWithPointers(text)", "yaml-eslint-parser": "parseYAML(text)",
             "yaml-js": "yaml.load(text)", "@visulima/yaml": "parseYaml(text)", "@amritk/yaml": "parseDocument(text)",
             "yaml-to-momoa": "yamlToMomoa(text)", "yaml.min": "parseYaml(text)"}


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class JavaScriptYamlPilotTest(unittest.TestCase):
    def selected(self):
        rows = read(BASE / "parsers.json")
        self.assertTrue(rows)
        return rows

    def test_controls_and_trees_match_hand_written_oracle(self):
        for row in self.selected():
            with self.subTest(package=row["name"]):
                project = ROOT / row["project"]
                manifest = read(project / "manifest.json")
                receipt = read(project / "verification.json")
                self.assertEqual(project.name, SLUGS[row["name"]])
                self.assertTrue(receipt["pass"])
                self.assertEqual(receipt["output"], manifest["expected_output"])
                self.assertEqual(row["expected_output"], manifest["expected_output"])
                for control, digest, output in (
                        ("control", "control_sha256", "expected_output"),
                        ("differential_control", "differential_control_sha256",
                         "differential_expected_output")):
                    data = (ROOT / manifest[control]).read_bytes()
                    self.assertEqual(sha256(data).hexdigest(), manifest[digest])
                    self.assertEqual(ORACLE["CONTROLS"][CONTROL_NAMES[manifest[control]]], manifest[digest])
                    self.assertEqual(manifest[output],
                                     {"tree": ORACLE["EXPECTED"][CONTROL_NAMES[manifest[control]]]})

    def test_release_lock_and_documented_api_are_pinned(self):
        for row in self.selected():
            with self.subTest(package=row["name"]):
                project = ROOT / row["project"]
                manifest = read(project / "manifest.json")
                lock = read(project / "source-lock.json")[row["name"]]
                npm_lock = read(project / "package-lock.json")["packages"][f"node_modules/{row['name']}"]
                self.assertEqual(lock["release"], row["version"])
                self.assertEqual(npm_lock["version"], row["version"])
                self.assertEqual(npm_lock["integrity"], row["npm_integrity"])
                self.assertEqual(lock["source_sha256"], row["tarball_sha256"])
                self.assertIn(row["tarball_sha256"], (project / "Dockerfile").read_text())
                self.assertIn(f"/blob/{DOC_TAGS[row['name']]}/", row["documentation"])
                adapter = (project / "adapter.mjs").read_text()
                self.assertIn("fatal: true", adapter)
                self.assertIn(API_CALLS[row["name"]], adapter)
                self.assertEqual(manifest["scope"], row["scope"])

    def test_wrappers_pin_and_cover_their_underlying_parser(self):
        for row in self.selected():
            if "underlying_package" not in row:
                continue
            with self.subTest(package=row["name"]):
                project = ROOT / row["project"]
                manifest = read(project / "manifest.json")
                receipt = read(project / "verification.json")
                npm_lock = read(project / "package-lock.json")["packages"][f"node_modules/{row['underlying_package']}"]
                lock = read(project / "source-lock.json")[row["underlying_package"]]
                self.assertTrue(row["family"].startswith("Wrapper:"))
                self.assertEqual(manifest["underlying_package"], row["underlying_package"])
                self.assertEqual(manifest["underlying_release"], row["underlying_version"])
                self.assertEqual(npm_lock["version"], row["underlying_version"])
                self.assertEqual(npm_lock["integrity"], row["underlying_npm_integrity"])
                self.assertEqual(lock["source_sha256"], row["underlying_tarball_sha256"])
                self.assertIn(row["underlying_tarball_sha256"], (project / "Dockerfile").read_text())
                self.assertGreater(receipt["parser_source_lines_covered"], 0)
                self.assertGreater(receipt["underlying_source_lines_covered"], 0)

    def test_parser_feedback_is_stable_and_input_dependent(self):
        for row in self.selected():
            with self.subTest(package=row["name"]):
                project = ROOT / row["project"]
                manifest = read(project / "manifest.json")
                feedback = read(ROOT / row["afl_feedback"])
                overlay = ROOT / "fuzzing/afl-native/yaml/javascript" / project.name / "verification.json"
                self.assertTrue(feedback["pass"])
                self.assertEqual(feedback["runs_per_control"], 3)
                self.assertTrue(feedback["repeated_control_identical"])
                self.assertTrue(feedback["repeated_differential_identical"])
                self.assertGreater(feedback["parser_feature_difference"], 0)
                self.assertGreater(feedback["afl_tuple_difference"], 0)
                self.assertEqual(feedback["overlay_receipt_sha256"], sha256(overlay.read_bytes()).hexdigest())
                self.assertEqual(read(overlay)["base_image_id"], read(project / "verification.json")["image_id"])
                self.assertEqual(feedback["control_sha256"], manifest["control_sha256"])
                self.assertEqual(feedback["differential_sha256"], manifest["differential_control_sha256"])

    def test_cell_counts_selected_rows_in_metric_order(self):
        rows = self.selected()
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(rows))
        values = [row["popularity"]["value"] for row in rows]
        self.assertEqual(values, sorted(values, reverse=True))
        leads = {lead["name"]: lead for lead in read(BASE / "leads.json")}
        for row in rows:
            self.assertEqual(leads[row["name"]]["status"], "selected")
            self.assertEqual(leads[row["name"]]["metric_value"], row["popularity"]["value"])

    def test_uncounted_leads_carry_evidence(self):
        probes = BASE / "round2-lead-probes.json"
        failing = ({item["package"] for item in read(probes)["probes"]
                    if not all(control["matches_oracle"] for control in item["controls"].values())}
                   if probes.is_file() else set())
        selected = {row["name"] for row in self.selected()}
        for lead in read(BASE / "leads.json"):
            with self.subTest(lead=lead["name"]):
                self.assertTrue(lead["reason"])
                self.assertEqual(lead["status"] == "selected", lead["name"] in selected)
                if lead.get("evidence"):
                    self.assertTrue((ROOT / lead["evidence"]).is_file())
                if lead["status"] == "excluded_control_failed" and lead.get("evidence") == str(probes.relative_to(ROOT)):
                    self.assertIn(lead["name"], failing)


if __name__ == "__main__":
    unittest.main()
