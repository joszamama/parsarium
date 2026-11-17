"""The JavaScript XML pilot keeps its selection, leads, receipts and feedback consistent."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/javascript/xml"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class JavaScriptXmlPilotTest(unittest.TestCase):
    def test_selected_parsers_are_ranked_and_leads_recorded(self):
        parsers = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")
        metrics = [parser["popularity"]["value"] for parser in parsers]
        self.assertEqual(metrics, sorted(metrics, reverse=True))
        selected = {parser["name"] for parser in parsers}
        self.assertTrue(selected.isdisjoint(
            {lead["name"] for lead in leads if lead["status"] == "unresolved"}))
        self.assertTrue(all(lead["status"] in {"unresolved", "promoted_to_verified"} for lead in leads))
        self.assertEqual({lead["name"] for lead in leads if lead["status"] == "promoted_to_verified"},
                         {"fast-xml-parser"})
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(cell["unresolved_documentation_leads"],
                         sum(lead["status"] == "unresolved" for lead in leads))
        downloads = read(BASE / "registry-snapshot.json")["downloads"]
        for parser in parsers:
            self.assertEqual(downloads[parser["name"]]["value"], parser["popularity"]["value"])

    def test_receipts_match_both_controls(self):
        verification = {entry["package"]: entry for entry in read(BASE / "verification.json")["third_party"]}
        feedback = {entry["project"]: entry for entry in read(BASE / "afl-feedback.json")["results"]}
        for parser in read(BASE / "parsers.json"):
            project = ROOT / parser["project"]
            manifest = read(project / "manifest.json")
            receipt = read(project / "verification.json")
            lock = read(project / "source-lock.json")[parser["name"]]
            self.assertEqual(lock["npm_integrity"], parser["npm_integrity"])
            self.assertEqual(lock["source_sha256"], parser["tarball_sha256"])
            self.assertTrue(receipt["pass"])
            self.assertEqual(receipt["output"], parser["expected_output"])
            self.assertEqual(verification[parser["name"]]["differential_output"],
                             manifest["differential_expected_output"])
            result = feedback[str(project.relative_to(ROOT / "projects"))]
            self.assertTrue(result["repeated_control_identical"] and result["repeated_differential_identical"])
            self.assertGreater(result["parser_feature_difference"], 0)
            self.assertGreater(result["afl_tuple_difference"], 0)


if __name__ == "__main__":
    unittest.main()
