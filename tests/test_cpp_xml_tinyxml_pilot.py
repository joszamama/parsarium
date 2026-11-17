"""The C++ TinyXML (v1) path keeps its pins, Expat oracle, metric rank and feedback consistent."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/cpp/xml"
PACKAGE = "tinyxml"
PROJECT = ROOT / "projects/xml/cpp/tinyxml"
OVERLAY = ROOT / "fuzzing/afl-native/xml/cpp/tinyxml"

_spec = importlib.util.spec_from_file_location("xml_check_controls", ROOT / "controls/xml/check_controls.py")
oracle = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(oracle)


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def entry(name: str, items: list, key: str = "name") -> dict:
    found, = [item for item in items if item[key] == name]
    return found


class CppXmlTinyXmlPilotTest(unittest.TestCase):
    def test_pins_agree(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        self.assertEqual((manifest["release"], lock["release"]), ("2.6.2", "2.6.2"))
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        for dockerfile in (PROJECT / "Dockerfile", OVERLAY / "Dockerfile"):
            text = dockerfile.read_text()
            for pinned in (lock["source_sha256"], lock["source_url"], manifest["base_image"]):
                self.assertIn(pinned, text)
        self.assertIn("-DTIXML_USE_STL", (PROJECT / "build.sh").read_text())
        self.assertIn("document.Parse(", (PROJECT / "harness.cpp").read_text())

    def test_expat_oracle_matches_both_shared_controls(self):
        manifest = read(PROJECT / "manifest.json")
        self.assertEqual(manifest["differential_control"], "controls/xml/order-default-ns.xml")
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
        record = entry(PACKAGE, read(BASE / "verification.json")["third_party"], "package")
        differential = read(OVERLAY / "differential.json")
        self.assertTrue(receipt["pass"] and record["pass"] and differential["pass"])
        for output in (receipt["output"], parser["expected_output"], record["output"]):
            self.assertEqual(output, manifest["expected_output"])
        self.assertEqual(record["second_valid_output"], manifest["differential_expected_output"])
        self.assertEqual(differential["second_control_output"], manifest["differential_expected_output"])
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)

    def test_metric_rank_family_and_leads(self):
        parsers = read(BASE / "parsers.json")
        parser = entry(PACKAGE, parsers)
        self.assertEqual(parser["popularity"]["dev_package_installs"], {"libtinyxml-dev": 533})
        values = [item["popularity"]["value"] for item in parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        self.assertIn("3.0%", parser["family_note"])
        snapshot = read(BASE / "registry-snapshot.json")
        row = entry("TinyXML", snapshot["candidates"], "library")
        self.assertEqual(row["dev_installs"], 533)
        search = snapshot["debian_dev_package_search"]
        self.assertEqual(search["snapshot_sha256"], snapshot["sources"]["popcon_binary_by_inst"]["sha256"])
        self.assertEqual(entry("libtinyxml-dev", search["rows"], "package")["decision"], "selected as tinyxml")
        leads = read(BASE / "leads.json")
        self.assertEqual(entry(PACKAGE, leads)["status"], "resolved_verified_selected")
        self.assertEqual(entry("Boost.PropertyTree", leads)["status"], "excluded")
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(cell["unresolved_documentation_leads"],
                         sum(item["status"] == "unresolved" for item in leads))

    def test_feedback_is_stable_and_differential(self):
        report = read(BASE / "afl-feedback.json")
        result = entry("xml/cpp/tinyxml", report["results"], "project")
        overlay = read(OVERLAY / "verification.json")
        self.assertEqual(sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
                         result["overlay_receipt_sha256"])
        self.assertEqual(sha256((OVERLAY / "differential.json").read_bytes()).hexdigest(),
                         result["differential_receipt_sha256"])
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertGreater(result["afl_tuple_difference"], 0)
        self.assertEqual(report["projects_total"], len(report["results"]))


if __name__ == "__main__":
    unittest.main()
