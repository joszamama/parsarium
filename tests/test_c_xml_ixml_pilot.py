"""The C ixml path keeps its pins, raw-name expat oracle, Debian binary-name search and feedback consistent."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/c/xml"
PACKAGE = "ixml"
PROJECT = ROOT / "projects/xml/c/ixml"
OVERLAY = ROOT / "fuzzing/afl-native/xml/c/ixml"

_spec = importlib.util.spec_from_file_location("ixml_oracle", PROJECT / "oracle.py")
oracle = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(oracle)


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def entry(name: str, items: list, key: str = "name") -> dict:
    found, = [item for item in items if item[key] == name]
    return found


class CXmlIxmlPilotTest(unittest.TestCase):
    def test_pins_agree(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        self.assertEqual((manifest["release"], lock["release"]), ("22.2.1", "22.2.1"))
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        for dockerfile in (PROJECT / "Dockerfile", OVERLAY / "Dockerfile"):
            text = dockerfile.read_text()
            for pinned in (lock["source_sha256"], lock["source_url"], manifest["base_image"]):
                self.assertIn(pinned, text)
        self.assertIn("ixmlParseBufferEx(text, &doc)", (PROJECT / "harness.c").read_text())

    def test_raw_name_oracle_matches_both_controls(self):
        manifest = read(PROJECT / "manifest.json")
        self.assertIs(manifest["namespace_resolution"], False)
        self.assertEqual((PROJECT / "oracle.py").read_bytes(),
                         (ROOT / "projects/xml/c/libxmlb/oracle.py").read_bytes())
        for control, digest, expected in (
                (manifest["control"], manifest["control_sha256"], manifest["expected_output"]),
                (manifest["differential_control"], manifest["differential_control_sha256"],
                 manifest["differential_expected_output"])):
            data = (ROOT / control).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), digest)
            self.assertEqual(oracle.summarize(data), expected, control)

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
        result = entry("xml/c/ixml", read(BASE / "afl-feedback.json")["results"], "project")
        self.assertTrue(result["pass"] and result["repeated_controls_identical"])
        self.assertGreater(result["afl_tuple_difference"], 0)
        self.assertEqual(result["second_control_output"], manifest["differential_expected_output"])
        self.assertEqual(result["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())

    def test_metric_rank_and_leads(self):
        parsers = read(BASE / "parsers.json")
        parser = entry(PACKAGE, parsers)
        snapshot = read(BASE / "registry-snapshot.json")
        candidate = snapshot["c_candidates"][PACKAGE]
        self.assertEqual(parser["metric"]["value"], candidate["primary_installed"])
        self.assertEqual(parser["metric"]["value"], 46966)
        self.assertEqual(candidate["debian_binary_packages"]["libixml22"]["installed"], 3781)
        values = [item["metric"]["value"] for item in parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        self.assertEqual([item["name"] for item in parsers][3:5], [PACKAGE, "mxml"])
        leads = read(BASE / "leads.json")["leads"]
        self.assertEqual(entry(PACKAGE, leads)["status"], "selected")
        self.assertEqual(entry("iksemel", leads)["status"], "unresolved_control_mismatch")
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(cell["leads_recorded"], len(leads))
        search = snapshot["debian_source_search"]
        self.assertEqual(search["total"], len(search["hits"]))
        self.assertEqual(sorted(hit["name"] for hit in search["hits"]
                                if hit["classification"] == "c_xml_parser_library"),
                         ["libnxml", "libxml2", "libxml2.9", "libxmlb", "mxml"])


if __name__ == "__main__":
    unittest.main()
