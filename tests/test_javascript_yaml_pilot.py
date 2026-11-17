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
SLUGS = {"js-yaml": "js_yaml", "yaml": "yaml"}


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
                self.assertIn(f"/blob/{'v' if row['name'] == 'yaml' else ''}{row['version']}/",
                              row["documentation"])
                adapter = (project / "adapter.mjs").read_text()
                self.assertIn("fatal: true", adapter)
                self.assertIn("jsyaml.load(text)" if row["name"] == "js-yaml" else "YAML.parseDocument(text)",
                              adapter)
                self.assertEqual(manifest["scope"], row["scope"])

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


if __name__ == "__main__":
    unittest.main()
