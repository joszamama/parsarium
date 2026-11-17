"""The C++ cxxtools XmlReader path keeps its pins, raw-name expat oracle, weak metric label and feedback consistent."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/cpp/xml"
PACKAGE = "cxxtools"
PROJECT = ROOT / "projects/xml/cpp/cxxtools"
OVERLAY = ROOT / "fuzzing/afl-native/xml/cpp/cxxtools"

_spec = importlib.util.spec_from_file_location("cxxtools_oracle", PROJECT / "oracle.py")
oracle = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(oracle)


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def entry(name: str, items: list, key: str = "name") -> dict:
    found, = [item for item in items if item[key] == name]
    return found


class CppXmlCxxtoolsPilotTest(unittest.TestCase):
    def test_pins_agree(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        self.assertEqual((manifest["release"], lock["release"]), ("3.0.0", "3.0.0"))
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        for dockerfile in (PROJECT / "Dockerfile", OVERLAY / "Dockerfile"):
            text = dockerfile.read_text()
            for pinned in (lock["source_sha256"], lock["source_url"], manifest["base_image"]):
                self.assertIn(pinned, text)
        self.assertIn("cxxtools::xml::XmlReader reader(input)", (PROJECT / "harness.cpp").read_text())

    def test_raw_name_oracle_matches_both_controls(self):
        manifest = read(PROJECT / "manifest.json")
        self.assertIs(manifest["namespace_resolution"], False)
        self.assertEqual((PROJECT / "oracle.py").read_bytes(),
                         (ROOT / "projects/xml/c/libnxml/oracle.py").read_bytes())
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
        for output in (parser["differential_expected_output"], record["second_valid_output"],
                       differential["second_control_output"]):
            self.assertEqual(output, manifest["differential_expected_output"])
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)

    def test_metric_rank_and_leads(self):
        parsers = read(BASE / "parsers.json")
        parser = entry(PACKAGE, parsers)
        self.assertEqual(parser["popularity"]["dev_package_installs"], {"libcxxtools-dev": 42})
        self.assertIn("Weak signal", parser["popularity"]["qualification"])
        self.assertEqual(parser["namespace_semantics"], "raw_names_only")
        values = [item["popularity"]["value"] for item in parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        self.assertEqual([item["name"] for item in parsers][-2:], [PACKAGE, "rapidxml"])
        snapshot = read(BASE / "registry-snapshot.json")
        self.assertEqual(entry("cxxtools", snapshot["candidates"], "library")["dev_installs"], 42)
        self.assertEqual(entry(PACKAGE, read(BASE / "leads.json"))["status"], "resolved_verified_selected")
        self.assertEqual(read(BASE / "cell.json")["verified_third_party_count"], len(parsers))

    def test_feedback_is_stable_and_differential(self):
        report = read(BASE / "afl-feedback.json")
        result = entry("xml/cpp/cxxtools", report["results"], "project")
        overlay = read(OVERLAY / "verification.json")
        self.assertEqual(sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
                         result["overlay_receipt_sha256"])
        self.assertEqual(sha256((OVERLAY / "differential.json").read_bytes()).hexdigest(),
                         result["differential_receipt_sha256"])
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertGreater(result["afl_tuple_difference"], 0)
        self.assertGreater(result["xmlreader_line_difference"], 0)


if __name__ == "__main__":
    unittest.main()
