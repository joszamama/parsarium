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
                lock = read(project / "source-lock.json")[row["module"]]
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
                self.assertTrue(set(result["difference_features_by_file"]) & {"scannerc.go", "parserc.go"})

    def test_v2_harness_keeps_mapping_order(self):
        if not any(row["name"] == "gopkg.in/yaml.v2" for row in self.parsers):
            self.skipTest("yaml.v2 not selected")
        harness = (ROOT / "projects/yaml/go/gopkg_in_yaml_v2/harness.go").read_text()
        self.assertIn("yaml.MapSlice", harness)
        self.assertIn("UnmarshalYAML", harness)


if __name__ == "__main__":
    unittest.main()
