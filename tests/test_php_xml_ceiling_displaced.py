"""PHP XML keeps ten paths by Packagist downloads; pear/xml_parser is archived as qualified but outside the ceiling."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/xml"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PhpXmlCeilingTest(unittest.TestCase):
    def test_ten_selected_in_download_order(self):
        parsers = read(BASE / "parsers.json")
        values = [row["popularity"]["value"] for row in parsers]
        self.assertEqual(len(parsers), 10)
        self.assertEqual(values, sorted(values, reverse=True))
        self.assertEqual(read(BASE / "cell.json")["verified_third_party_count"], 10)

    def test_pear_xml_parser_is_archived_not_selected(self):
        archive = read(BASE / "ceiling-displaced.json")
        path, = archive["paths"]
        parsers = read(BASE / "parsers.json")
        self.assertEqual(path["name"], "pear/xml_parser")
        self.assertNotIn("pear/xml_parser", [row["name"] for row in parsers])
        self.assertLess(path["downloads"], parsers[-1]["popularity"]["value"])
        self.assertEqual(archive["tenth_selected"], {"name": parsers[-1]["name"],
                                                     "downloads": parsers[-1]["popularity"]["value"]})
        for key in ("removed_project", "removed_overlay", "removed_verify_script", "removed_test", "removed_guide"):
            self.assertFalse((ROOT / path[key]).exists(), path[key])
        self.assertTrue((ROOT / path["feedback_differential_receipt"]).is_file())
        self.assertTrue(path["project_receipt"]["pass"] and path["overlay_receipt"]["pass"])
        lead, = [row for row in read(BASE / "leads.json") if row["name"] == "pear/xml_parser"]
        self.assertEqual(lead["status"], "qualified_but_ten_path_ceiling")
        report = [row["project"] for row in read(BASE / "afl-feedback.json")["results"]]
        self.assertNotIn("xml/php/pear_xml_parser", report)

    def test_classification_covers_hits_above_the_eleventh_path(self):
        snapshot = read(BASE / "registry-snapshot.json")
        leads = {row["name"] for row in read(BASE / "leads.json")}
        classified = {row["name"] for row in snapshot["classification_2026_11_18"]["rows"]}
        threshold = snapshot["classification_2026_11_18"]["threshold_downloads"]
        hits = {hit["name"] for query in snapshot["search"] for hit in query["hits"] if hit["downloads"] >= threshold}
        self.assertEqual(hits - leads - classified, set())


if __name__ == "__main__":
    unittest.main()
