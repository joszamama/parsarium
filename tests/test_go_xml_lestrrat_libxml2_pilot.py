"""The Go lestrrat-go/libxml2 cgo path keeps its pins, patch, summaries, family and native feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/go/xml"
PACKAGE = "github.com/lestrrat-go/libxml2"
RELEASE = "v0.0.0-20260709020957-3f0f7bd60b63"
SLUG = "github_com_lestrrat_go_libxml2"
PROJECT = ROOT / "projects/xml/go" / SLUG
OVERLAY = ROOT / "fuzzing/afl-native/xml/go" / SLUG
GOKOGIRI = ROOT / "projects/xml/go/github_com_moovweb_gokogiri"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class GoXmlLestratLibxml2PilotTest(unittest.TestCase):
    def test_pins_and_patch_agree(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        go_sum = (PROJECT / "go.sum").read_text()
        self.assertEqual((manifest["release"], lock["release"]), (RELEASE, RELEASE))
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        for digest in (lock["source_sha256"], lock["license_file_sha256"], lock["binding_source_sha256"],
                       lock["compatibility_patch_sha256"], lock["underlying_source_sha256"],
                       manifest["base_image"]):
            self.assertIn(digest, dockerfile)
        self.assertEqual(sha256((PROJECT / "cgo-compat.patch").read_bytes()).hexdigest(),
                         lock["compatibility_patch_sha256"])
        patch = (PROJECT / "cgo-compat.patch").read_text()
        self.assertEqual(sum(line.startswith("+") and not line.startswith("+++")
                             for line in patch.splitlines()), 1)
        self.assertIn(f"{PACKAGE} {RELEASE} {lock['go_module_sum']}", go_sum)
        # Same native libxml2 pin and configure line as the gokogiri path.
        self.assertEqual(manifest["underlying_source_sha256"],
                         read(GOKOGIRI / "manifest.json")["underlying_source_sha256"])
        self.assertEqual((PROJECT / "afl-allowlist.txt").read_bytes(),
                         (GOKOGIRI / "afl-allowlist.txt").read_bytes())
        for name in ("catalog-ns.xml", "order-default-ns.xml"):
            self.assertEqual((PROJECT / "controls" / name).read_bytes(),
                             (ROOT / "controls/xml" / name).read_bytes())

    def test_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        record, = [item for item in read(BASE / "verification.json")["third_party"]
                   if item["package"] == PACKAGE]
        goxpp, = [item for item in read(BASE / "verification.json")["third_party"]
                  if item["package"] == "github.com/mmcdole/goxpp"]
        self.assertTrue(receipt["pass"] and record["pass"] and record["differential_pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        self.assertEqual(record["output"], goxpp["output"])
        self.assertEqual(manifest["differential_expected_output"], goxpp["differential_output"])
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        self.assertGreater(receipt["parser_source_lines_covered"], 20)
        self.assertGreater(receipt["underlying_source_lines_covered"], 100)
        self.assertEqual(parser["popularity"]["value"], 30)
        self.assertEqual(parser["shared_families"], ["libxml2 XML parser"])

    def test_native_feedback_is_stable_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        validation = read(OVERLAY / "feedback-validation.json")
        self.assertEqual(overlay["feedback_kind"], "go_cgo_libxml2_native_xml_parser_edges")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        for name, digest in overlay["overlay_file_sha256"].items():
            self.assertEqual(sha256((OVERLAY / name).read_bytes()).hexdigest(), digest, name)
        self.assertTrue(validation["pass"] and validation["repeat_maps_identical"]
                        and validation["parse_only_and_full_maps_identical"])
        self.assertEqual(validation["repeats_per_control"], 5)
        self.assertEqual(validation["post_parse_tuples"], 0)
        self.assertGreater(validation["native_tuple_difference"], 1)
        self.assertEqual(validation["first_native_tuples"], overlay["feedback_edges"])
        self.assertEqual(validation["second_control_output"], manifest["differential_expected_output"])
        self.assertFalse(validation["mutation_campaign_run"])

    def test_leads_and_family(self):
        leads = {lead["name"]: lead for lead in read(BASE / "leads.json")}
        self.assertEqual(leads[PACKAGE]["status"], "promoted_to_verified")
        self.assertEqual(leads["github.com/lestrrat/go-libxml2"]["status"], "excluded")
        family, = [item for item in read(BASE / "verification.json")["shared_families"]
                   if item["family"] == "libxml2 XML parser (Go cgo bindings)"]
        self.assertEqual(len(family["paths"]), 2)


if __name__ == "__main__":
    unittest.main()
