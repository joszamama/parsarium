"""The mellium.im/xmlstream negative lead keeps its pins, oracle result and feedback finding consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROBE = ROOT / "lead-probes/go/xml/xmlstream"
RECEIPT = ROOT / "data/go/xml/xmlstream-lead-check.json"
GOXPP = ROOT / "projects/xml/go/github_com_mmcdole_goxpp"
CONTROLS = ("catalog-ns.xml", "order-default-ns.xml")


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class GoXmlXmlstreamLeadTest(unittest.TestCase):
    def setUp(self):
        self.receipt = read(RECEIPT)

    def test_pins_agree(self):
        receipt = self.receipt
        check = (PROBE / "check.py").read_text()
        go_sum = (PROBE / "go.sum").read_text()
        self.assertEqual((receipt["package"], receipt["release"]), ("mellium.im/xmlstream", "v0.15.4"))
        for digest in (receipt["module_zip_sha256"], receipt["license_file_sha256"],
                       receipt["underlying_source_sha256"], receipt["image"]):
            self.assertIn(digest, check)
        self.assertIn(f"mellium.im/xmlstream v0.15.4 {receipt['module_sum']}", go_sum)
        self.assertIn(f"mellium.im/xmlstream v0.15.4/go.mod {receipt['go_mod_sum']}", go_sum)
        # encoding/xml is the same pinned source the goxpp project measures.
        self.assertEqual(receipt["underlying_source_sha256"],
                         read(GOXPP / "source-lock.json")["github.com/mmcdole/goxpp"]["underlying_source_sha256"])
        for name, digest in receipt["probe_file_sha256"].items():
            self.assertEqual(sha256((PROBE / name).read_bytes()).hexdigest(), digest, name)
        self.assertEqual(receipt["popularity"]["value"], 86)

    def test_oracle_paths_match_shared_result(self):
        catalog = read(GOXPP / "manifest.json")["expected_output"]
        for mode in ("readall", "iter"):
            controls = self.receipt["modes"][mode]["controls"]
            self.assertEqual(controls["catalog-ns.xml"]["observed"], catalog)
            for control in CONTROLS:
                self.assertTrue(controls[control]["matches_shared_namespace_oracle"])
        for control in CONTROLS:
            inner = self.receipt["modes"]["innerreader"]["controls"][control]["observed"]
            self.assertIn("error", inner["control"])
            self.assertNotIn("error", inner["trailing_whitespace_trimmed"])

    def test_negative_decision_follows_feedback(self):
        receipt = self.receipt
        self.assertTrue(receipt["status"].startswith("negative_lead"))
        self.assertIsNone(receipt["api_finding"]["local_bytes_parse_api"])
        for mode in ("readall", "iter"):
            record = receipt["modes"][mode]
            self.assertTrue(record["repeated_runs_identical"])
            self.assertEqual(record["xmlstream_block_difference"], 0)
            self.assertEqual(record["changed_xmlstream_blocks"], [])
            self.assertGreater(record["encoding_xml_block_difference"], 0)
            for control in CONTROLS:
                self.assertGreater(record["controls"][control]["xmlstream_cover_blocks"], 0)
        self.assertEqual(receipt["afl_feedback"], "not_built_no_xmlstream_differential")


if __name__ == "__main__":
    unittest.main()
