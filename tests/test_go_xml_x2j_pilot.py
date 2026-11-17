"""The Go beego/x2j XML path keeps its pins, oracle check, family and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/go/xml"
PACKAGE = "github.com/beego/x2j"
RELEASE = "v0.0.0-20131220205130-a0352aadc542"
PROJECT = ROOT / "projects/xml/go/github_com_beego_x2j"
OVERLAY = ROOT / "fuzzing/afl-native/xml/go/github_com_beego_x2j"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def record() -> dict:
    item, = [item for item in read(BASE / "verification.json")["third_party"]
             if item["package"] == PACKAGE]
    return item


class GoXmlX2jPilotTest(unittest.TestCase):
    def test_pins_agree(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        go_sum = (PROJECT / "go.sum").read_text()
        self.assertEqual((manifest["release"], lock["release"]), (RELEASE, RELEASE))
        self.assertTrue(RELEASE.endswith(lock["git_commit"][:12]))
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        for digest in (lock["source_sha256"], lock["license_sha256"], lock["parser_source_sha256"],
                       lock["reader_source_sha256"], manifest["base_image"]):
            self.assertIn(digest, dockerfile)
        self.assertIn(f"{PACKAGE} {RELEASE} {lock['go_module_sum']}", go_sum)
        self.assertIn(f"{PACKAGE} {RELEASE}/go.mod {lock['go_mod_sum']}", go_sum)
        self.assertIn("-coverpkg=github.com/beego/x2j,encoding/xml", dockerfile)

    def test_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        item = record()
        self.assertTrue(receipt["pass"] and item["pass"] and item["differential_pass"])
        for output in (receipt["output"], parser["expected_output"], item["output"]):
            self.assertEqual(output, manifest["expected_output"])
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        # x2j's own XML-to-map code is covered, separately from encoding/xml.
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertEqual(item["parser_source_lines_covered"], receipt["parser_source_lines_covered"])
        self.assertEqual(item["encoding_xml_lines_covered"], receipt["underlying_source_lines_covered"])
        self.assertEqual(parser["popularity"]["value"], 436)

    def test_byte_and_reader_paths_differ_as_documented(self):
        output = read(PROJECT / "manifest.json")["expected_output"]
        self.assertIn("catalog/item[1]/note=x< y", output["bytes"]["text"])
        self.assertIn("catalog/item[1]/note=x < y", output["reader"]["text"])
        self.assertIn("catalog/#text=3", output["reader"]["lists"])
        harness = (PROJECT / "harness_test.go").read_text(encoding="utf-8")
        for value in record()["differential_output"]["bytes"]["attributes"]:
            self.assertIn(json.dumps(value, ensure_ascii=False)[1:-1], harness)

    def test_oracle_check_is_current(self):
        check = read(BASE / "x2j-oracle-check.json")
        self.assertTrue(check["pass"])
        self.assertEqual(check["oracle_script_sha256"],
                         sha256((ROOT / "scripts/verify_go_xml_x2j_oracle.py").read_bytes()).hexdigest())
        self.assertEqual(check["manifest_sha256"],
                         sha256((PROJECT / "manifest.json").read_bytes()).hexdigest())
        results = {item["control"]: item for item in check["results"]}
        self.assertEqual(set(results), {"controls/xml/catalog-ns.xml", "controls/xml/order-default-ns.xml"})
        empty = {"oracle_only": [], "x2j_only": []}
        for item in results.values():
            self.assertEqual(item["reader_mismatches"], empty)
        self.assertEqual(results["controls/xml/order-default-ns.xml"]["bytes_mismatches"], empty)
        self.assertEqual(results["controls/xml/catalog-ns.xml"]["bytes_mismatches"],
                         {"oracle_only": ["catalog/item[1]/note=x < y"],
                          "x2j_only": ["catalog/item[1]/note=x< y"]})

    def test_family_is_shared_and_leads_resolved(self):
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        self.assertEqual(parser["shared_families"], ["Go encoding/xml Decoder tokenizer"])
        self.assertIn("not an independent tokenizer", parser["family_note"])
        family, = [item for item in read(BASE / "verification.json")["shared_families"]
                   if item["family"] == "Go encoding/xml Decoder tokenizer"]
        self.assertIn("github.com/beego/x2j (via Decoder.Token)", family["paths"])
        leads = {lead["name"] for lead in read(BASE / "leads.json")}
        self.assertNotIn(PACKAGE, leads)
        self.assertIn("github.com/clbanning/x2j", leads)
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(read(BASE / "parsers.json")))
        self.assertEqual(cell["unresolved_documentation_leads"], len(leads))

    def test_feedback_is_stable_and_differential_in_both_layers(self):
        report = read(BASE / "afl-feedback.json")
        result, = [item for item in report["results"]
                   if item["project"] == "xml/go/github_com_beego_x2j"]
        overlay = read(OVERLAY / "verification.json")
        self.assertEqual(sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
                         result["overlay_receipt_sha256"])
        self.assertTrue(result["pass"] and result["repeated_control_identical"])
        self.assertTrue(result["underlying_repeated_control_identical"])
        self.assertEqual(result["underlying_subject_prefix"], "encoding/xml/")
        for key in ("parser_feature_difference", "afl_tuple_difference",
                    "underlying_feature_difference", "underlying_afl_tuple_difference"):
            self.assertGreater(result[key], 0, key)
        self.assertEqual(result["control_parser_features"], overlay["parser_source_features"])
        self.assertIn("ENV PARSARIUM_SUBJECT_PREFIX=github.com/beego/x2j/",
                      (OVERLAY / "Dockerfile").read_text())


if __name__ == "__main__":
    unittest.main()
