"""The Go go-pkg-xmlx XML path keeps its pins, summaries, family and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/go/xml"
PACKAGE = "github.com/go-forks/go-pkg-xmlx"
RELEASE = "v0.0.0-20151201012946-76f54ee73233"
SLUG = "github_com_go_forks_go_pkg_xmlx"
PROJECT = ROOT / "projects/xml/go" / SLUG
OVERLAY = ROOT / "fuzzing/afl-native/xml/go" / SLUG


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class GoXmlXmlxPilotTest(unittest.TestCase):
    def test_pins_agree(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        go_sum = (PROJECT / "go.sum").read_text()
        self.assertEqual((manifest["release"], lock["release"]), (RELEASE, RELEASE))
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        for digest in (lock["source_sha256"], lock["license_file_sha256"], lock["parser_source_sha256"],
                       lock["underlying_source_sha256"], manifest["base_image"]):
            self.assertIn(digest, dockerfile)
        self.assertIn(f"{PACKAGE} {RELEASE} {lock['go_module_sum']}", go_sum)
        self.assertIn(f"{PACKAGE} {RELEASE}/go.mod {lock['go_mod_sum']}", go_sum)
        self.assertIn("-coverpkg=github.com/go-forks/go-pkg-xmlx,encoding/xml", dockerfile)

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
        # Same expat-oracle summaries as the other namespace-aware Go paths.
        goxpp, = [item for item in read(BASE / "verification.json")["third_party"]
                  if item["package"] == "github.com/mmcdole/goxpp"]
        self.assertEqual(record["output"], goxpp["output"])
        self.assertEqual(record["differential_output"], goxpp["differential_output"])
        self.assertEqual(sha256((ROOT / manifest["control"]).read_bytes()).hexdigest(),
                         manifest["control_sha256"])
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        self.assertGreater(receipt["parser_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        self.assertEqual(parser["popularity"]["value"], 20)

    def test_family_and_leads(self):
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        self.assertEqual(parser["shared_families"], ["Go encoding/xml Decoder tokenizer"])
        family, = [item for item in read(BASE / "verification.json")["shared_families"]
                   if item["family"] == "Go encoding/xml Decoder tokenizer"]
        self.assertIn(f"{PACKAGE} (via Decoder.Token)", family["paths"])
        lead, = [item for item in read(BASE / "leads.json") if item["name"] == PACKAGE]
        self.assertEqual(lead["status"], "promoted_to_verified")
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(read(BASE / "parsers.json")))

    def test_feedback_is_stable_and_differential(self):
        overlay = read(OVERLAY / "verification.json")
        differential = read(OVERLAY / "differential.json")
        report = read(BASE / "afl-feedback.json")
        result, = [item for item in report["results"] if item["project"] == f"xml/go/{SLUG}"]
        digest = sha256((OVERLAY / "verification.json").read_bytes()).hexdigest()
        self.assertEqual(result["overlay_receipt_sha256"], digest)
        self.assertEqual(differential["overlay_receipt_sha256"], digest)
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        for item in (result, differential):
            self.assertTrue(item["pass"] and item["repeated_control_identical"])
            self.assertGreater(item["parser_feature_difference"], 0)
            self.assertGreater(item["underlying_feature_difference"], 0)
            self.assertEqual(item["control_parser_features"], overlay["parser_source_features"])
        self.assertTrue(differential["differential_control_pass"]
                        and differential["repeated_differential_identical"])
        self.assertTrue(all(block.startswith(PACKAGE + "/document.go:")
                            for block in differential["changed_xmlx_source_blocks"]))
        self.assertIn(f"ENV PARSARIUM_SUBJECT_PREFIX={PACKAGE}/", (OVERLAY / "Dockerfile").read_text())


if __name__ == "__main__":
    unittest.main()
