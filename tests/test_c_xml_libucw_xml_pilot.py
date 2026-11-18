"""The C libucw-xml path keeps its pins, namespace-aware expat oracle, metric and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/c/xml"
PACKAGE = "libucw-xml"
SLUG = "libucw_xml"
PROJECT = ROOT / "projects/xml/c" / SLUG
OVERLAY = ROOT / "fuzzing/afl-native/xml/c" / SLUG


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def entry(name: str, items: list, key: str = "name") -> dict:
    found, = [item for item in items if item[key] == name]
    return found


class CXmlLibucwXmlPilotTest(unittest.TestCase):
    def test_pins_agree(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        self.assertEqual((manifest["release"], lock["release"]), ("6.5", "6.5"))
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        for dockerfile in (PROJECT / "Dockerfile", OVERLAY / "Dockerfile"):
            text = dockerfile.read_text()
            for pinned in (lock["source_sha256"], lock["source_url"], manifest["base_image"]):
                self.assertIn(pinned, text)
        self.assertIn("xml_ns_enable(", (PROJECT / "harness.c").read_text())

    def test_expected_outputs_follow_the_shared_oracle(self):
        manifest = read(PROJECT / "manifest.json")
        self.assertIs(manifest["namespace_resolution"], True)
        expat = read(ROOT / "projects/xml/c/expat/manifest.json")
        for key in ("expected_output", "differential_expected_output"):
            shared = dict(expat[key])
            pass
            self.assertEqual(manifest[key], shared)
        for control, digest in ((manifest["control"], manifest["control_sha256"]),
                                (manifest["differential_control"], manifest["differential_control_sha256"])):
            self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)

    def test_receipts_match_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser = entry(PACKAGE, read(BASE / "parsers.json"))
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        self.assertEqual(parser["differential_expected_output"], manifest["differential_expected_output"])
        self.assertEqual(parser["version"], manifest["release"])
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        overlay = read(OVERLAY / "verification.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        result = entry("xml/c/" + SLUG, read(BASE / "afl-feedback.json")["results"], "project")
        self.assertTrue(result["pass"] and result["repeated_controls_identical"])
        self.assertGreater(result["afl_tuple_difference"], 0)
        self.assertEqual(result["second_control_output"], manifest["differential_expected_output"])
        self.assertEqual(result["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())

    def test_metric_and_rank(self):
        parsers = read(BASE / "parsers.json")
        parser = entry(PACKAGE, parsers)
        candidate = read(BASE / "registry-snapshot.json")["c_candidates"][PACKAGE]
        self.assertEqual(parser["metric"]["value"], candidate["primary_installed"])
        self.assertEqual(parser["metric"]["value"], 60)
        values = [item["metric"]["value"] for item in parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        self.assertEqual(entry(PACKAGE, read(BASE / "leads.json")["leads"])["status"], "selected")
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(parsers))


if __name__ == "__main__":
    unittest.main()
