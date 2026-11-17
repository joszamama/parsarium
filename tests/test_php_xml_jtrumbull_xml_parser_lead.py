"""jtrumbull/xml-parser and orchestra/parser are negative PHP XML leads with no parsing route of their own."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/xml"
PROBE = ROOT / "lead-probes/php/xml/jtrumbull_xml_parser"
CHECK = BASE / "jtrumbull-xml-parser-lead-check.json"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class PhpXmlNegativeWrapperLeadsTest(unittest.TestCase):
    def test_jtrumbull_decode_is_a_bare_simplexml_json_round_trip(self):
        check = read(CHECK)
        self.assertEqual(check["status"], "negative_lead_simplexml_json_round_trip")
        lead, = [item for item in read(BASE / "leads.json") if item["name"] == check["package"]]
        self.assertEqual(lead["status"], "excluded")
        self.assertEqual((lead["version_seen"], lead["packagist_downloads"], lead["license"]),
                         (check["release"], check["popularity"]["value"], check["license"]))
        self.assertNotIn(check["package"], {item["name"] for item in read(BASE / "parsers.json")})
        self.assertFalse((ROOT / "projects/xml/php/jtrumbull_xml_parser").exists())
        locked, = read(PROBE / "composer.lock")["packages"]
        self.assertEqual((locked["version"], locked["dist"]["reference"]),
                         (check["release"], check["composer_reference"]))
        self.assertIn(check["archive_sha256"], (PROBE / "Dockerfile").read_text())
        for name, digest in check["probe_file_sha256"].items():
            self.assertEqual(sha256((PROBE / name).read_bytes()).hexdigest(), digest, name)
        for name, digest in check["control_sha256"].items():
            self.assertEqual(sha256((ROOT / "controls/xml" / name).read_bytes()).hexdigest(), digest)
            self.assertIs(check["observed"][name]["identical_to_bare_simplexml_json"], True)
        self.assertEqual(check["observed"]["catalog-ns.xml"]["package_lines"],
                         {"lib/XMLParser/XMLParser.php": [137, 139, 141]})
        self.assertTrue(check["afl_feedback"].startswith("not_run"))

    def test_orchestra_parser_is_excluded_as_laravie_bridge(self):
        leads = {item["name"]: item for item in read(BASE / "leads.json")}
        orchestra = leads["orchestra/parser"]
        self.assertEqual(orchestra["status"], "excluded")
        self.assertIn("7dfe57ee9cbf07853e09f620689e35e9f883b6ba", orchestra["reason"])
        self.assertIn("laravie/parser", orchestra["reason"])
        self.assertEqual(leads["laravie/parser"]["status"], "excluded")
        self.assertNotIn("orchestra/parser", {item["name"] for item in read(BASE / "parsers.json")})


if __name__ == "__main__":
    unittest.main()
