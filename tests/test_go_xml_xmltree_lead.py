"""The aqwari.net/xml/xmltree negative lead keeps its pins, oracle result and feedback finding consistent."""

from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "lead-probes/go/xml/xmltree"
RECEIPT = ROOT / "data/go/xml/xmltree-lead-check.json"
CONTROLS = ("controls/xml/catalog-ns.xml", "controls/xml/order-default-ns.xml")


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class GoXmlXmltreeLeadTest(unittest.TestCase):
    def setUp(self):
        self.receipt = read(RECEIPT)

    def test_pins_agree(self):
        receipt = self.receipt
        lock = read(PROBE / "source-lock.json")["aqwari.net/xml/xmltree"]
        dockerfile = (PROBE / "Dockerfile").read_text()
        go_sum = (PROBE / "go.sum").read_text()
        self.assertEqual(receipt["release"], lock["release"])
        for digest in (lock["source_sha256"], *lock["files_sha256"].values(),
                       *(item["zip_sha256"] for item in lock["dependencies"].values()),
                       receipt["underlying_source_sha256"], receipt["image"].split("@")[1]):
            self.assertIn(digest, dockerfile)
        self.assertIn(f"aqwari.net/xml {lock['release']} {lock['go_module_sum']}", go_sum)
        for module, item in lock["dependencies"].items():
            self.assertIn(f"{module} {item['release']} {item['go_module_sum']}", go_sum)
        for name, digest in receipt["probe_file_sha256"].items():
            self.assertEqual(sha256((PROBE / name).read_bytes()).hexdigest(), digest, name)
        self.assertEqual(receipt["popularity"]["value"], 43)
        snapshot = (ROOT / "data/go/xml/registry-snapshot.json").read_text()
        self.assertIn('"packagePath": "aqwari.net/xml/xmltree"', snapshot)

    def test_oracle_matches_receipt(self):
        oracle = json.loads(subprocess.run(
            [sys.executable, "-I", str(PROBE / "oracle.py"), *CONTROLS],
            check=True, capture_output=True, text=True).stdout)
        harness_test = (PROBE / "harness_test.go").read_text()
        for control in CONTROLS:
            record = self.receipt["controls"][control]
            self.assertTrue(record["matches_expat_oracle"])
            self.assertEqual(record["observed"], oracle[control])
            self.assertIn(json.dumps(oracle[control], ensure_ascii=False, sort_keys=True,
                                     separators=(",", ":")), harness_test)
            self.assertEqual(record["control_sha256"], sha256((ROOT / control).read_bytes()).hexdigest())
            self.assertGreater(record["xmltree_source_lines"], 0)
            self.assertGreater(record["encoding_xml_source_lines"], 0)

    def test_negative_decision_follows_feedback(self):
        receipt = self.receipt
        self.assertEqual(receipt["status"], "negative_lead_no_package_feedback_differential")
        own = receipt["fixed_differential_feedback"]["xmltree"]
        self.assertEqual((own["afl_parser_feature_difference"], own["afl_tuple_difference"],
                          own["replay_cover_block_difference"]), (0, 0, 0))
        self.assertGreater(own["control_afl_features"], 0)
        self.assertGreater(receipt["fixed_differential_feedback"]["encoding_xml"]["afl_parser_feature_difference"], 0)
        for record in receipt["supplementary_input_dependence"].values():
            self.assertGreater(record["xmltree_feature_difference_vs_control"], 0)
        self.assertFalse((ROOT / "projects/xml/go/xmltree").exists())


if __name__ == "__main__":
    unittest.main()
