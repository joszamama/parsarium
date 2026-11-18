"""The C++ RapidXML path keeps its pins, Expat oracle, weak metric label and feedback consistent."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/cpp/xml"
PACKAGE = "rapidxml"
PROJECT = ROOT / "projects/xml/cpp/rapidxml"
OVERLAY = ROOT / "fuzzing/afl-native/xml/cpp/rapidxml"

_spec = importlib.util.spec_from_file_location("xml_check_controls", ROOT / "controls/xml/check_controls.py")
oracle = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(oracle)


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def entry(name: str, items: list, key: str = "name") -> dict:
    found, = [item for item in items if item[key] == name]
    return found


class CppXmlRapidXmlPilotTest(unittest.TestCase):
    def test_pins_agree(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        self.assertEqual((manifest["release"], lock["release"]), ("1.13", "1.13"))
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        for dockerfile in (PROJECT / "Dockerfile", OVERLAY / "Dockerfile"):
            text = dockerfile.read_text()
            for pinned in (lock["source_sha256"], lock["source_url"], manifest["base_image"]):
                self.assertIn(pinned, text)
        self.assertEqual((PROJECT / "afl-allowlist.txt").read_text().split(), ["src:rapidxml.hpp"])
        self.assertIn("parse<0>(", (PROJECT / "parser-probe.cpp").read_text())
        self.assertIn("parse<0>(", (PROJECT / "harness.cpp").read_text())

    def test_expat_oracle_matches_both_controls(self):
        manifest = read(PROJECT / "manifest.json")
        for control, digest, expected in (
                (manifest["control"], manifest["control_sha256"], manifest["expected_output"]),
                (manifest["differential_control"], manifest["differential_control_sha256"],
                 manifest["differential_expected_output"])):
            data = (ROOT / control).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), digest)
            self.assertEqual(oracle.summarize(data), expected, control)
        # RapidXML uses the shared order control, processing instruction included.
        self.assertEqual(manifest["differential_control"], "controls/xml/order-default-ns.xml")

    def test_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser = entry(PACKAGE, read(BASE / "parsers.json"))
        record = entry(PACKAGE, read(BASE / "verification.json")["third_party"], "package")
        differential = read(OVERLAY / "differential.json")
        self.assertTrue(receipt["pass"] and record["pass"])
        for output in (receipt["output"], parser["expected_output"], record["output"]):
            self.assertEqual(output, manifest["expected_output"])
        self.assertEqual(record["second_valid_output"], manifest["differential_expected_output"])
        self.assertEqual(differential["second_observed_output"], manifest["differential_expected_output"])
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        self.assertEqual(receipt["parser_source_lines_covered"], 413)
        self.assertEqual(record["parser_source_lines_covered"], receipt["parser_source_lines_covered"])

    def test_weak_metric_rank_from_snapshot(self):
        parser = entry(PACKAGE, read(BASE / "parsers.json"))
        popularity = parser["popularity"]
        self.assertEqual(popularity["value"], 17)
        self.assertEqual(popularity["dev_package_installs"], {"librapidxml-dev": 17})
        self.assertEqual(popularity["recent_use_votes"], 0)
        self.assertIn("Weak signal", popularity["qualification"])
        snapshot = read(BASE / "registry-snapshot.json")
        row = entry("RapidXML", snapshot["candidates"], "library")
        self.assertEqual(row["dev_installs"], popularity["value"])
        self.assertEqual(snapshot["primary_order_by_dev_installs"][-2:], ["RapidXML", "libcutl"])
        installs = [entry(name, snapshot["candidates"], "library")["dev_installs"]
                    for name in snapshot["primary_order_by_dev_installs"]]
        self.assertEqual(installs, sorted(installs, reverse=True))
        ranking = (BASE / "ranking.md").read_text(encoding="utf-8")
        self.assertIn("| 9 | [RapidXML]", ranking)
        self.assertIn("none with recent use", ranking)

    def test_family_and_counts(self):
        parsers = read(BASE / "parsers.json")
        parser = entry(PACKAGE, parsers)
        self.assertIn("Boost.PropertyTree", parser["family_note"])
        self.assertEqual([item["family"] for item in parsers].count(parser["family"]), 1)
        cell = read(BASE / "cell.json")
        leads = read(BASE / "leads.json")
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(entry(PACKAGE, leads)["status"], "resolved_verified_selected")
        self.assertEqual(cell["unresolved_documentation_leads"],
                         sum(item["status"] == "unresolved" for item in leads))
        self.assertFalse((BASE / "rapidxml-candidate.json").exists())

    def test_feedback_is_stable_and_differential(self):
        report = read(BASE / "afl-feedback.json")
        result = entry("xml/cpp/rapidxml", report["results"], "project")
        differential = read(OVERLAY / "differential.json")
        overlay = read(OVERLAY / "verification.json")
        self.assertEqual(sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
                         result["overlay_receipt_sha256"])
        self.assertEqual(sha256((OVERLAY / "differential.json").read_bytes()).hexdigest(),
                         result["differential_receipt_sha256"])
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertTrue(result["pass"] and differential["repeated_feedback_identical"])
        self.assertEqual(differential["repeats_per_control"], 3)
        self.assertEqual(differential["second_case_kind"], "valid_control")
        self.assertEqual((result["control_afl_tuples"], result["differential_afl_tuples"],
                          result["afl_tuple_difference"]), (38, 45, 15))
        self.assertGreater(result["source_line_difference"], 0)
        self.assertEqual(report["projects_total"], len(report["results"]))


if __name__ == "__main__":
    unittest.main()
