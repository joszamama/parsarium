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
        parser, = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")
        metric = parser["popularity"]["value"]
        self.assertNotIn(f"{parser['group']}:{parser['artifact']}", {lead["coordinate"] for lead in leads})
        self.assertTrue(all(lead["status"] in {"unresolved", "not_a_parser_engine"} for lead in leads))
        self.assertTrue(all(metric > lead["summed_direct_dependent_count"]
                            for lead in leads if lead["status"] == "unresolved"))
        snapshot = read(BASE / "registry-snapshot.json")
        recorded = snapshot["popularity_metric"]["packages"][f"{parser['group']}:{parser['artifact']}"]
        self.assertEqual(recorded["summed_direct_dependent_count"], metric)
        self.assertEqual(snapshot["releases"]["xerces:xercesImpl"]["sources_sha256"],
                         read(ROOT / parser["project"] / "manifest.json")["source_sha256"])
        cell = read(BASE / "cell.json")
        self.assertEqual(sum(lead["status"] == "unresolved" for lead in leads),
                         cell["unresolved_documentation_leads"])

    def test_both_paths_share_the_xerces_family(self):
        parser, = read(BASE / "parsers.json")
        api, = read(BASE / "standard.json")["verified_apis"]
        self.assertIn("Apache Xerces2-J", parser["shared_families"])
        self.assertIn("Xerces2-J", api["family"])

    def test_control_receipts_match_catalog(self):
        parser, = read(BASE / "parsers.json")
        api, = read(BASE / "standard.json")["verified_apis"]
        for slug, expected in (("xercesimpl", parser["expected_output"]),
                               ("jdk_documentbuilder", api["expected"])):
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
        self.assertEqual(report["projects_passed"], 2)
        for result in report["results"]:
            overlay = ROOT / "fuzzing/afl-native" / result["project"] / "verification.json"
            self.assertEqual(sha256(overlay.read_bytes()).hexdigest(), result["overlay_receipt_sha256"])
            self.assertTrue(result["pass"] and result["repeated_control_identical"])
            self.assertGreater(result["parser_feature_difference"], 0)
            self.assertGreater(result["afl_tuple_difference"], 0)
            self.assertEqual(result["differential_output"], oracle)


if __name__ == "__main__":
    unittest.main()
