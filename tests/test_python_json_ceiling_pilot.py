"""Python JSON paths displaced by the ten-path ceiling and excluded leads stay recorded with evidence."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/json"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PythonJsonCeilingPilotTest(unittest.TestCase):
    def test_selected_paths_fill_the_ceiling_in_metric_order(self):
        parsers = read(BASE / "parsers.json")
        cell = read(BASE / "cell.json")
        self.assertEqual([parser["name"] for parser in parsers],
                         ["pydantic", "jiter", "orjson", "json5", "simplejson", "ijson", "msgspec", "ujson",
                          "dirtyjson", "hjson"])
        self.assertEqual(len(parsers), cell["ceiling"])
        self.assertEqual(cell["ceiling_displaced"], "data/python/json/ceiling-displaced.json")

    def test_displaced_paths_rank_below_the_tenth_and_keep_evidence(self):
        parsers = read(BASE / "parsers.json")
        leads = {lead["name"]: lead for lead in read(BASE / "leads.json")["leads"]}
        record = read(BASE / "ceiling-displaced.json")
        tenth = parsers[-1]
        self.assertEqual(record["status"], "qualified_but_ten_path_ceiling")
        self.assertEqual(record["tenth_selected"], {"name": tenth["name"],
                                                    "last_month": leads[tenth["name"]]["last_month"]})
        selected = {parser["name"] for parser in parsers}
        self.assertEqual([path["name"] for path in record["paths"]], ["python-rapidjson", "pysimdjson"])
        for path in record["paths"]:
            name = path["name"]
            self.assertNotIn(name, selected)
            self.assertEqual(leads[name]["status"], "qualified_but_ten_path_ceiling")
            self.assertEqual(path["last_month"], leads[name]["last_month"])
            self.assertLess(path["last_month"], record["tenth_selected"]["last_month"])
            self.assertGreater(path["displaced_by_last_month"], path["last_month"])
            self.assertIn(path["displaced_by"], selected)
            self.assertTrue(path["verification_record"]["pass"])
            self.assertEqual(path["catalog_row"]["name"], name)
            self.assertEqual(path["catalog_row"]["popularity"]["value"], path["last_month"])
            receipt = ROOT / path["valid_feedback_receipt"]
            self.assertEqual(sha256(receipt.read_bytes()).hexdigest(), path["valid_feedback_receipt_sha256"])
            self.assertTrue(read(receipt)["pass"])
            for removed in ("removed_project", "removed_overlay", "removed_verify_script", "removed_test"):
                self.assertFalse((ROOT / path[removed]).exists(), path[removed])
        statuses = [lead["status"] for lead in leads.values()]
        self.assertEqual(statuses.count("qualified_but_ten_path_ceiling"), len(record["paths"]))

    def test_unrun_leads_below_the_tenth_and_json_repair_exclusion(self):
        parsers = read(BASE / "parsers.json")
        leads = {lead["name"]: lead for lead in read(BASE / "leads.json")["leads"]}
        tenth = leads[parsers[-1]["name"]]["last_month"]
        for lead in leads.values():
            if lead["status"] == "lead":
                self.assertLess(lead["last_month"], tenth, lead["name"])
        repair = leads["json-repair"]
        self.assertEqual(repair["status"], "excluded")
        self.assertEqual(repair["lead_kind"], "delegates_to_stdlib_json_on_valid_input")
        self.assertIn("skip_json_loads=True", repair["reason"])
        release = read(BASE / "registry-snapshot.json")["releases"]["json-repair"]
        self.assertEqual(release["version"], repair["version_seen"])


if __name__ == "__main__":
    unittest.main()
