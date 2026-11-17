"""C YAML pilot paths keep their pins, oracle trees, metric and parser-scoped AFL++ feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import runpy
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/c/yaml"
ORACLE = runpy.run_path(str(ROOT / "controls/yaml/check_controls.py"))
POPCON_SHA256 = "9d5e341c8ede7267acab176e255be83aca763f09901477eef5324d644cdaebf8"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class CYamlPilotTest(unittest.TestCase):
    def setUp(self):
        self.parsers = read(BASE / "parsers.json")
        self.cell = read(BASE / "cell.json")

    def test_cell_counts_selected_rows_in_metric_order(self):
        self.assertEqual(self.cell["verified_third_party_count"], len(self.parsers))
        values = [row["popularity"]["value"] for row in self.parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        leads = {lead["name"]: lead for lead in read(BASE / "leads.json")}
        for row in self.parsers:
            self.assertEqual(leads[row["name"]]["status"], "selected")
            self.assertEqual(leads[row["name"]]["metric_value"], row["popularity"]["value"])
            self.assertEqual(row["popularity"]["source_sha256"], POPCON_SHA256)
        snapshot = read(BASE / "registry-snapshot.json")
        self.assertEqual(snapshot["search"][0]["snapshot_sha256"], POPCON_SHA256)

    def test_pins_and_scoped_afl_sources(self):
        for row in self.parsers:
            with self.subTest(row["name"]):
                project = ROOT / row["project"]
                overlay = ROOT / "fuzzing/afl-native/yaml/c" / row["name"]
                manifest = read(project / "manifest.json")
                lock = read(project / "source-lock.json")[row["name"]]
                self.assertEqual({manifest["release"], lock["release"], row["version"]}, {row["version"]})
                self.assertEqual({manifest["source_sha256"], lock["source_sha256"], row["source_sha256"]},
                                 {lock["source_sha256"]})
                for dockerfile in (project / "Dockerfile", overlay / "Dockerfile"):
                    text = dockerfile.read_text()
                    for pinned in (lock["source_sha256"], lock["source"], manifest["base_image"]):
                        self.assertIn(pinned, text)
                allowlist = (project / "afl-allowlist.txt").read_text().split()
                self.assertTrue(allowlist and all(item.startswith("src:") for item in allowlist))
                self.assertNotIn("harness.c", " ".join(allowlist))
                feedback = read(overlay / "differential.json")
                self.assertEqual(feedback["allowlist_entries"], allowlist)
                self.assertNotIn("parser-probe.o", feedback["afl_instrumented_objects"])

    def test_outputs_equal_hand_written_oracle_trees(self):
        verification = {item["package"]: item for item in read(BASE / "verification.json")["third_party"]}
        for row in self.parsers:
            with self.subTest(row["name"]):
                project = ROOT / row["project"]
                manifest = read(project / "manifest.json")
                receipt = read(project / "verification.json")
                for control, digest, expected in (
                        (manifest["control"], manifest["control_sha256"], manifest["expected_output"]),
                        (manifest["differential_control"], manifest["differential_control_sha256"],
                         manifest["differential_expected_output"])):
                    self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)
                    tree = ORACLE["EXPECTED"][Path(control).name]
                    self.assertEqual(expected["tree"], tree)
                    self.assertEqual(expected["tree_sha256"], ORACLE["tree_sha256"](tree))
                self.assertTrue(receipt["pass"])
                self.assertEqual(receipt["output"], manifest["expected_output"])
                self.assertEqual(row["expected_output"], manifest["expected_output"])
                self.assertEqual(verification[row["name"]]["output"], manifest["expected_output"])
                self.assertIn("adapter-side", row["typing_caveat"])

    def test_feedback_is_stable_and_control_dependent(self):
        for row in self.parsers:
            with self.subTest(row["name"]):
                project = ROOT / row["project"]
                overlay = ROOT / "fuzzing/afl-native/yaml/c" / row["name"]
                feedback = read(overlay / "differential.json")
                self.assertTrue(feedback["pass"])
                self.assertEqual(feedback["repeats_per_control"], 3)
                self.assertTrue(feedback["repeated_feedback_identical"])
                self.assertGreater(feedback["parser_line_difference"], 0)
                self.assertGreater(feedback["afl_tuple_difference"], 0)
                self.assertEqual(feedback["base_project_receipt_sha256"],
                                 sha256((project / "verification.json").read_bytes()).hexdigest())
                self.assertEqual(feedback["overlay_receipt_sha256"],
                                 sha256((overlay / "verification.json").read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
