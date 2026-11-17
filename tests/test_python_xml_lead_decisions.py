"""Python XML lead decisions stay consistent with the bounded search snapshot and the rapidxml probe."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/xml"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PythonXmlLeadDecisionTest(unittest.TestCase):
    def setUp(self):
        self.leads = read(BASE / "leads.json")["leads"]
        self.snapshot = read(BASE / "registry-snapshot.json")
        self.parsers = read(BASE / "parsers.json")

    def test_metrics_come_from_one_snapshot(self):
        packages = self.snapshot["download_metric"]["packages"]
        for lead in self.leads:
            self.assertEqual(lead["last_month"], packages[lead["name"]]["downloads"], lead["name"])
        self.assertEqual(self.snapshot["search_limit_per_query"], 100)
        for query in self.snapshot["search"]:
            self.assertLessEqual(len(query["hits"]), 100)
            self.assertEqual(len(query["hits"]), min(query["total"], 100))
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["search_hits_recorded"], sum(len(query["hits"]) for query in self.snapshot["search"]))
        self.assertEqual(cell["registry_snapshot"], "data/python/xml/registry-snapshot.json")

    def test_selected_rows_follow_the_metric_and_every_higher_lead_is_decided(self):
        values = [parser["popularity"]["value"] for parser in self.parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        floor = min(values)
        for lead in self.leads:
            if lead["last_month"] >= floor:
                self.assertIn(lead["status"], {"promoted_to_verified", "excluded"}, lead["name"])
            if lead["status"] == "excluded":
                self.assertTrue(lead["reason"], lead["name"])
        selected = {parser["name"] for parser in self.parsers}
        self.assertEqual(selected, {lead["name"] for lead in self.leads if lead["status"] == "promoted_to_verified"})
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(self.parsers))
        self.assertIn("tenth slot is open", cell["uncertainty"])

    def test_rapidxml_probe_matches_reason(self):
        receipt = read(BASE / "rapidxml-lead-check.json")
        probe = ROOT / "lead-probes/python/xml/rapidxml"
        for name, digest in receipt["probe_file_sha256"].items():
            self.assertEqual(sha256((probe / name).read_bytes()).hexdigest(), digest, name)
        catalog = receipt["observed"]["controls/xml/catalog-ns.xml"]
        order = receipt["observed"]["controls/xml/order-default-ns.xml"]
        self.assertNotIn("x < y", catalog["default"]["text"])
        self.assertIn("x < y", catalog["parse_cdata"]["text"])
        self.assertFalse(order["default"]["ok"])
        self.assertTrue(order["parse_cdata"]["ok"])
        lead, = [lead for lead in self.leads if lead["name"] == "rapidxml"]
        self.assertEqual(lead["status"], "excluded")


if __name__ == "__main__":
    unittest.main()
