"""The Java XML pilot keeps its selection, leads, runtime path and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/java/xml"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class JavaXmlPilotTest(unittest.TestCase):
    def test_selected_parser_is_highest_parser_engine_lead(self):
        parsers = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")
        metrics = [parser["popularity"]["value"] for parser in parsers]
        self.assertEqual(metrics, sorted(metrics, reverse=True))
        selected = {f"{parser['group']}:{parser['artifact']}" for parser in parsers}
        self.assertTrue(selected.isdisjoint(
            {lead["coordinate"] for lead in leads if lead["status"] == "unresolved"}))
        self.assertTrue(all(lead["status"] in {"unresolved", "not_a_parser_engine",
                                               "promoted_to_verified"} for lead in leads))
        self.assertEqual({lead["coordinate"] for lead in leads
                          if lead["status"] == "promoted_to_verified"},
                         {"com.fasterxml.woodstox:woodstox-core"})
        self.assertTrue(all(min(metrics) > lead["summed_direct_dependent_count"]
                            for lead in leads if lead["status"] == "unresolved"))
        snapshot = read(BASE / "registry-snapshot.json")
        for parser in parsers:
            coordinate = f"{parser['group']}:{parser['artifact']}"
            recorded = snapshot["popularity_metric"]["packages"][coordinate]
            self.assertEqual(recorded["summed_direct_dependent_count"],
                             parser["popularity"]["value"])
        xerces = next(parser for parser in parsers if parser["artifact"] == "xercesImpl")
        self.assertEqual(snapshot["releases"]["xerces:xercesImpl"]["sources_sha256"],
                         read(ROOT / xerces["project"] / "manifest.json")["source_sha256"])
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(sum(lead["status"] == "unresolved" for lead in leads),
                         cell["unresolved_documentation_leads"])

    def test_both_paths_share_the_xerces_family(self):
        parsers = read(BASE / "parsers.json")
        xerces = next(parser for parser in parsers if parser["artifact"] == "xercesImpl")
        woodstox = next(parser for parser in parsers if parser["artifact"] == "woodstox-core")
        api, = read(BASE / "standard.json")["verified_apis"]
        self.assertIn("Apache Xerces2-J", xerces["shared_families"])
        self.assertNotIn("Apache Xerces2-J", woodstox["shared_families"])
        self.assertIn("Woodstox", woodstox["shared_families"])
        self.assertIn("Xerces2-J", api["family"])

    def test_control_receipts_match_catalog(self):
        parsers = read(BASE / "parsers.json")
        api, = read(BASE / "standard.json")["verified_apis"]
        paths = [(Path(parser["project"]).name, parser["expected_output"])
                 for parser in parsers]
        paths.append(("jdk_documentbuilder", api["expected"]))
        for slug, expected in paths:
            project = ROOT / "projects/xml/java" / slug
            manifest = read(project / "manifest.json")
            receipt = read(project / "verification.json")
            self.assertTrue(receipt["pass"])
            self.assertEqual(receipt["output"], expected)
            self.assertGreater(receipt["parser_source_lines_covered"], 0)
            self.assertEqual(sha256((ROOT / manifest["control"]).read_bytes()).hexdigest(),
                             manifest["control_sha256"])
            for name, digest in receipt["project_file_sha256"].items():
                self.assertEqual(sha256((project / name).read_bytes()).hexdigest(), digest, name)

    def test_feedback_is_stable_and_differential(self):
        report = read(BASE / "afl-feedback.json")
        oracle = read(ROOT / "data/go/xml/verification.json")["differential_output"]
        self.assertEqual(report["projects_passed"], len(read(BASE / "parsers.json")) + 1)
        self.assertEqual({item["project"] for item in report["results"]},
                         {"xml/java/xercesimpl", "xml/java/woodstox_core",
                          "xml/java/jdk_documentbuilder"})
        for result in report["results"]:
            overlay = ROOT / "fuzzing/afl-native" / result["project"] / "verification.json"
            self.assertEqual(sha256(overlay.read_bytes()).hexdigest(), result["overlay_receipt_sha256"])
            self.assertTrue(result["pass"] and result["repeated_control_identical"])
            self.assertGreater(result["parser_feature_difference"], 0)
            self.assertGreater(result["afl_tuple_difference"], 0)
            self.assertEqual(result["differential_output"], oracle)


if __name__ == "__main__":
    unittest.main()
