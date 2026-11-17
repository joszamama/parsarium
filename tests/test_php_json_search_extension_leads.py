"""PHP JSON supplemental Packagist search and the excluded bcncommerce/symfony lead probes."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/json"
PROBES = ROOT / "lead-probes/php/json"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class PhpJsonSearchExtensionTest(unittest.TestCase):
    def test_supplemental_search_is_bounded_and_counted(self):
        snapshot = read(BASE / "registry-snapshot.json")
        cell = read(BASE / "cell.json")
        extra = snapshot["supplemental_search"]
        searches = snapshot["search"] + extra["search"]
        self.assertEqual(extra["search_limit_per_query"], 100)
        self.assertTrue(all(len(query["hits"]) <= query["limit"] == 100 for query in extra["search"]))
        self.assertEqual(cell["search_queries"], [query["query"] for query in searches])
        self.assertEqual(cell["search_hits_recorded"], sum(len(query["hits"]) for query in searches))
        self.assertEqual(cell["unique_search_hits"],
                         len({hit["name"] for query in searches for hit in query["hits"]}))
        self.assertEqual(extra["combined_unique_hits"], cell["unique_search_hits"])

    def test_lead_statuses_and_downloads_come_from_the_snapshots(self):
        snapshot = read(BASE / "registry-snapshot.json")
        primary = {hit["name"]: hit["downloads"] for query in snapshot["search"] for hit in query["hits"]}
        extra = {hit["name"]: hit["downloads"]
                 for query in snapshot["supplemental_search"]["search"] for hit in query["hits"]}
        leads = read(BASE / "leads.json")
        cell = read(BASE / "cell.json")
        parsers = {item["name"] for item in read(BASE / "parsers.json")}
        self.assertEqual(cell["leads_recorded"], len(leads))
        self.assertEqual(cell["leads_by_status"],
                         {status: sum(lead["status"] == status for lead in leads)
                          for status in cell["leads_by_status"]})
        self.assertEqual(sum(cell["leads_by_status"].values()), len(leads))
        self.assertFalse({lead["name"] for lead in leads} & parsers)
        for lead in leads:
            source = extra if lead.get("downloads_snapshot") == "supplemental_search" else primary
            self.assertEqual(lead["packagist_downloads"], source[lead["name"]], lead["name"])

    def test_excluded_probes_fail_the_oracle_and_have_no_line_differential(self):
        leads = {lead["name"]: lead for lead in read(BASE / "leads.json")}
        for slug, package in (("bcncommerce_json_stream", "bcncommerce/json-stream"),
                              ("symfony_json_streamer", "symfony/json-streamer")):
            report = read(ROOT / leads[package]["evidence"])
            self.assertEqual(leads[package]["status"], "excluded")
            self.assertEqual(report["package"], package)
            for name, digest in report["probe_file_sha256"].items():
                self.assertEqual(sha256((PROBES / slug / name).read_bytes()).hexdigest(), digest)
            dockerfile = (PROBES / slug / "Dockerfile").read_text()
            self.assertIn(report["archive_url"], dockerfile)
            self.assertIn(f"{report['archive_sha256']}  /work/parser-source.zip", dockerfile)
            self.assertTrue(report["repeated_runs_identical"])
            self.assertEqual(report["package_line_difference"], 0)
            for item in report["observed"]:
                data = (ROOT / item["control"]).read_bytes()
                self.assertEqual(sha256(data).hexdigest(), item["control_sha256"])
                self.assertFalse(item["tree_matches_oracle"])
                self.assertNotEqual(item["tree"], item["oracle_tree"])
            # The nested-object control's empty object comes back as an empty PHP list.
            nested = dict(report["observed"][0]["tree"]["members"])["nested"]
            self.assertEqual(dict(nested["members"])["empty"], {"type": "php_list", "items": []})
        symfony = read(BASE / "symfony-json-streamer-lead-check.json")
        generated = symfony["observed"][0]["generated_reader"]
        self.assertIn("Decoder::decodeStream($stream, 0, null)", generated)
        bcn = read(BASE / "bcncommerce-json-stream-lead-check.json")
        version = dict(bcn["observed"][0]["tree"]["members"])["version"]
        self.assertEqual(version, {"type": "float", "value": 1.0})


if __name__ == "__main__":
    unittest.main()
