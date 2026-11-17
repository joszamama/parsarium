"""The Go mxj XML path keeps its pins, map summaries, family and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/go/xml"
PACKAGE = "github.com/clbanning/mxj"
PROJECT = ROOT / "projects/xml/go/github_com_clbanning_mxj"
OVERLAY = ROOT / "fuzzing/afl-native/xml/go/github_com_clbanning_mxj"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class GoXmlMxjPilotTest(unittest.TestCase):
    def test_pins_agree(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        go_sum = (PROJECT / "go.sum").read_text()
        self.assertEqual((manifest["release"], lock["release"]), ("v1.8.4", "v1.8.4"))
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        for digest in (lock["source_sha256"], lock["license_sha256"], lock["parser_source_sha256"],
                       manifest["base_image"]):
            self.assertIn(digest, dockerfile)
        self.assertIn(f"{PACKAGE} v1.8.4 {lock['go_module_sum']}", go_sum)
        self.assertIn(f"{PACKAGE} v1.8.4/go.mod {lock['go_mod_sum']}", go_sum)
        self.assertIn("-coverpkg=github.com/clbanning/mxj,encoding/xml", dockerfile)

    def test_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        record, = [item for item in read(BASE / "verification.json")["third_party"]
                   if item["package"] == PACKAGE]
        self.assertTrue(receipt["pass"] and record["pass"] and record["differential_pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        self.assertEqual(record["output"], manifest["expected_output"])
        self.assertEqual(sha256((ROOT / manifest["control"]).read_bytes()).hexdigest(),
                         manifest["control_sha256"])
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        # Own XML-to-map code is covered, not only the adapter or encoding/xml.
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertEqual(receipt["format_specific_source_lines_covered"],
                         receipt["parser_source_lines_covered"])
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        self.assertEqual(parser["popularity"]["value"], 553)

    def test_differential_summary_is_pinned_in_harness(self):
        record, = [item for item in read(BASE / "verification.json")["third_party"]
                   if item["package"] == PACKAGE]
        harness = (PROJECT / "harness_test.go").read_text(encoding="utf-8")
        for value in record["differential_output"]["attributes"]:
            self.assertIn(json.dumps(value, ensure_ascii=False)[1:-1], harness)
        self.assertEqual(record["differential_output"]["empty_elements"], ["order/line[1]/plain/leaf"])

    def test_family_is_shared_and_lead_resolved(self):
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        self.assertEqual(parser["shared_families"], ["Go encoding/xml Decoder tokenizer"])
        self.assertIn("not an independent tokenizer", parser["family_note"])
        family, = [item for item in read(BASE / "verification.json")["shared_families"]
                   if item["family"] == "Go encoding/xml Decoder tokenizer"]
        self.assertIn("github.com/clbanning/mxj (via Decoder.Token)", family["paths"])
        leads = {lead["name"] for lead in read(BASE / "leads.json")}
        self.assertNotIn(PACKAGE, leads)
        self.assertIn(f"{PACKAGE}/v2", leads)
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(read(BASE / "parsers.json")))
        self.assertEqual(cell["unresolved_documentation_leads"], len(leads))

    def test_feedback_is_stable_and_differential(self):
        report = read(BASE / "afl-feedback.json")
        result, = [item for item in report["results"]
                   if item["project"] == "xml/go/github_com_clbanning_mxj"]
        overlay = read(OVERLAY / "verification.json")
        self.assertEqual(sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
                         result["overlay_receipt_sha256"])
        self.assertTrue(result["pass"] and result["repeated_control_identical"])
        self.assertGreater(result["parser_feature_difference"], 0)
        self.assertGreater(result["afl_tuple_difference"], 0)
        self.assertEqual(result["control_parser_features"], overlay["parser_source_features"])
        self.assertIn("ENV PARSARIUM_SUBJECT_PREFIX=github.com/clbanning/mxj/",
                      (OVERLAY / "Dockerfile").read_text())


if __name__ == "__main__":
    unittest.main()
