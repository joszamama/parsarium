"""colinodell/json5 is excluded: valid JSON controls route to ext/json, not the package's parser."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/json"
PROBE = ROOT / "lead-probes/php/json/colinodell_json5"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class PhpJsonColinodellJson5LeadTest(unittest.TestCase):
    def test_lead_is_excluded_with_pinned_probe_evidence(self):
        check = read(BASE / "colinodell-json5-lead-check.json")
        lead, = [item for item in read(BASE / "leads.json") if item["name"] == "colinodell/json5"]
        self.assertEqual(lead["status"], "excluded")
        self.assertEqual(lead["evidence"], "data/php/json/colinodell-json5-lead-check.json")
        self.assertEqual((lead["version_seen"], lead["packagist_downloads"]),
                         (check["release"], check["popularity"]["value"]))
        self.assertNotIn("colinodell/json5", {item["name"] for item in read(BASE / "parsers.json")})
        locked, = read(PROBE / "composer.lock")["packages"]
        self.assertEqual((locked["version"], locked["source"]["reference"]),
                         (check["release"], check["composer_reference"]))
        dockerfile = (PROBE / "Dockerfile").read_text()
        self.assertIn(check["archive_sha256"], dockerfile)
        self.assertIn(check["composer_reference"], dockerfile)
        for name, digest in check["probe_file_sha256"].items():
            self.assertEqual(sha256((PROBE / name).read_bytes()).hexdigest(), digest, name)

    def test_both_controls_and_apis_ran_only_the_json_decode_delegation(self):
        check = read(BASE / "colinodell-json5-lead-check.json")
        for name, digest in check["control_sha256"].items():
            self.assertEqual(sha256((ROOT / "controls/json" / name).read_bytes()).hexdigest(), digest)
        runs = {(run["control"], run["api"]): run for run in check["observed"]}
        self.assertEqual(set(runs), {(control, api) for control in check["control_sha256"]
                                     for api in ("Json5Decoder::decode", "json5_decode")})
        self.assertTrue(check["type_tagged_trees_match_oracle"])
        self.assertEqual(check["own_parser_lines_executed"], 0)
        for run in runs.values():
            self.assertTrue(run["identical_to_json_decode"])
            decoder = set(run["package_lines_executed"]["src/Json5Decoder.php"]) - {593}
            self.assertEqual(decoder, {56, 57, 58})
        self.assertEqual(runs["nested-array.json", "json5_decode"]["tree"]["type"], "array")
        self.assertEqual(runs["nested-object.json", "Json5Decoder::decode"]["tree"]["type"], "object")


if __name__ == "__main__":
    unittest.main()
