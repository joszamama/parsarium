"""Keep xmlbuilder2's native namespace failure visible in the XML lead log."""

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/javascript/xml"


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


class Xmlbuilder2NegativeLeadTest(unittest.TestCase):
    def test_native_namespace_failure_prevents_selection(self):
        lead, = (item for item in read(BASE / "leads.json") if item["name"] == "xmlbuilder2")
        selected = {item["name"] for item in read(BASE / "parsers.json")}
        evidence = read(ROOT / lead["negative_evidence"])
        snapshot = read(BASE / "registry-snapshot.json")
        self.assertEqual(lead["status"], "excluded")
        self.assertNotIn("xmlbuilder2", selected)
        self.assertEqual(lead["npm_downloads_30d"], snapshot["downloads"]["xmlbuilder2"]["value"])
        self.assertEqual(evidence["candidate_npm_integrity"],
                         snapshot["latest_release_inspection"]["xmlbuilder2"]["integrity"])
        self.assertEqual(evidence["candidate_tarball_sha256"],
                         snapshot["latest_release_inspection"]["xmlbuilder2"]["tarball_sha256"])
        self.assertEqual(evidence["decision"], "excluded_from_selected_xml_1_0_namespaces_cell")
        native = evidence["native_observed"]
        self.assertEqual(native["root"]["name"], "c:catalog")
        self.assertEqual(native["root"]["namespace_uri"], "urn:parsarium:item")
        self.assertEqual(native["first_item_attributes"][1]["name"], "c:lang")
        self.assertIsNone(native["first_item_attributes"][1]["namespace_uri"])
        self.assertEqual(evidence["expat_oracle"]["root"], "{urn:parsarium:catalog}catalog")


if __name__ == "__main__":
    unittest.main()
