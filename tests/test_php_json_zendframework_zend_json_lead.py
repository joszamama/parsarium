"""zendframework/zend-json is excluded: ext/json by default, laminas-json Decoder lineage when opted in."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/json"
PROBE = ROOT / "lead-probes/php/json/zendframework_zend_json"
DEFAULT = "Zend\\Json\\Json::decode"
BUILTIN = "Zend\\Json\\Json::decode with $useBuiltinEncoderDecoder = true"
LAMINAS = "Laminas\\Json\\Json::decode with $useBuiltinEncoderDecoder = true"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class PhpJsonZendframeworkZendJsonLeadTest(unittest.TestCase):
    def test_lead_has_pinned_probe_evidence_and_is_not_a_parser_row(self):
        check = read(BASE / "zendframework-zend-json-lead-check.json")
        self.assertEqual(check["status"], "excluded_shared_laminas_decoder_family")
        lead, = [item for item in read(BASE / "leads.json") if item["name"] == "zendframework/zend-json"]
        self.assertEqual((lead["version_seen"], lead["packagist_downloads"], lead["license"]),
                         (check["release"], check["popularity"]["value"], check["license"]))
        self.assertNotIn("zendframework/zend-json", {item["name"] for item in read(BASE / "parsers.json")})
        locked, = read(PROBE / "composer.lock")["packages"]
        self.assertEqual((locked["version"], locked["source"]["reference"]),
                         (check["release"], check["composer_reference"]))
        dockerfile = (PROBE / "Dockerfile").read_text()
        self.assertIn(check["archive_sha256"], dockerfile)
        self.assertIn(check["composer_reference"], dockerfile)
        laminas = read(ROOT / "projects/json/php/laminas_json/source-lock.json")["laminas/laminas-json"]
        self.assertEqual(check["successor_reference"]["archive_sha256"], laminas["source_sha256"])
        self.assertIn(laminas["source_sha256"], dockerfile)
        for name, digest in check["probe_file_sha256"].items():
            self.assertEqual(sha256((PROBE / name).read_bytes()).hexdigest(), digest, name)

    def test_default_delegates_and_opt_in_runs_the_laminas_decoder_methods(self):
        check = read(BASE / "zendframework-zend-json-lead-check.json")
        for name, digest in check["control_sha256"].items():
            self.assertEqual(sha256((ROOT / "controls/json" / name).read_bytes()).hexdigest(), digest)
        runs = {(run["control"], run["route"]): run for run in check["observed"]}
        self.assertEqual(set(runs), {(control, route) for control in check["control_sha256"]
                                     for route in (DEFAULT, BUILTIN, LAMINAS)})
        self.assertTrue(check["type_tagged_trees_match_oracle"])
        self.assertEqual(check["decoder_methods"]["Zend\\Json\\Decoder"],
                         check["decoder_methods"]["Laminas\\Json\\Decoder"])
        for control in check["control_sha256"]:
            trees = {runs[control, route]["tree"] == runs[control, DEFAULT]["tree"]
                     for route in (BUILTIN, LAMINAS)}
            self.assertEqual(trees, {True})
            self.assertEqual(runs[control, DEFAULT]["package_lines_executed"],
                             {"src/Json.php": [47, 48, 49, 290, 292, 293, 294]})
            builtin = runs[control, BUILTIN]
            self.assertEqual(builtin["package_lines_executed"]["src/Json.php"], [47, 48, 52])
            self.assertEqual(set(builtin["package_methods_executed"]["src/Decoder.php"]),
                             set(runs[control, LAMINAS]["package_methods_executed"]["src/Decoder.php"]))
        self.assertEqual(runs["nested-array.json", DEFAULT]["tree"]["type"], "array")
        self.assertEqual(runs["nested-object.json", BUILTIN]["tree"]["type"], "object")


if __name__ == "__main__":
    unittest.main()
