"""smol-toml is a JavaScript TOML path whose typed tree comes from parse(text, {integersAsBigInt: true})."""

from hashlib import sha256
import json
from pathlib import Path
import sys
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/javascript/toml"
SLUG, NAME = "smol_toml", "smol-toml"
PROJECT = ROOT / "projects/toml/javascript" / SLUG
OVERLAY = ROOT / "fuzzing/afl-native/toml/javascript" / SLUG
sys.path.insert(0, str(ROOT / "controls/toml"))
from check_controls import typed  # noqa: E402


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class JavaScriptTomlSmolTomlTest(unittest.TestCase):
    def setUp(self):
        self.manifest = read(PROJECT / "manifest.json")
        self.receipt = read(PROJECT / "verification.json")
        self.parser, = [item for item in read(BASE / "parsers.json") if item["name"] == NAME]

    def test_both_controls_match_expected_trees_and_tomllib(self):
        trees = read(PROJECT / "expected-trees.json")
        report = read(BASE / f"{NAME}-tree-verification.json")
        self.assertTrue(self.receipt["pass"] and report["pass"])
        self.assertEqual(report["base_image_id"], self.receipt["image_id"])
        for key, expected_key in (("control", "expected_output"),
                                  ("differential_control", "differential_expected_output")):
            path = ROOT / self.manifest[key]
            digest = sha256(path.read_bytes()).hexdigest()
            self.assertEqual(digest, self.manifest[f"{key}_sha256"])
            committed = read(path.with_name(path.name.replace(".toml", ".expected.json")))
            self.assertEqual(self.manifest[expected_key], committed)
            self.assertEqual(trees[digest]["tree"], committed)
            self.assertEqual(typed(tomllib.loads(path.read_text(encoding="utf-8"))), committed)
        self.assertEqual([item["control"] for item in report["results"]],
                         [self.manifest["control"], self.manifest["differential_control"]])
        self.assertTrue(all(item["tree_matches_expected"] for item in report["results"]))
        self.assertEqual(self.receipt["output"], self.manifest["expected_output"])
        self.assertEqual(self.parser["expected_output"], self.manifest["expected_output"])
        self.assertEqual(self.receipt["control_sha256"], self.manifest["control_sha256"])

    def test_release_lock_license_and_metric(self):
        lock = read(PROJECT / "source-lock.json")[NAME]
        npm = read(PROJECT / "package-lock.json")["packages"][f"node_modules/{NAME}"]
        self.assertEqual((lock["release"], lock["npm_integrity"], lock["license"]),
                         (npm["version"], npm["integrity"], npm["license"]))
        self.assertEqual((self.parser["version"], self.parser["npm_integrity"], self.parser["tarball_sha256"],
                          self.parser["license"]),
                         (lock["release"], lock["npm_integrity"], lock["source_sha256"], lock["license"]))
        self.assertEqual(self.manifest["source_sha256"], lock["source_sha256"])
        dockerfile = (PROJECT / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn(lock["source_sha256"], dockerfile)
        self.assertIn(self.manifest["base_image"], dockerfile)
        snapshot = read(BASE / "registry-snapshot.json")["adoption_metric"]["packages"][NAME]
        self.assertEqual(self.parser["metric"]["value"], snapshot["downloads"])
        self.assertNotIn(NAME, [lead["name"] for lead in read(BASE / "leads.json")["leads"]])
        self.assertIn("smol-toml", self.parser["family"])

    def test_adapter_uses_documented_bigint_option_without_fallback(self):
        adapter = (PROJECT / "adapter.mjs").read_text(encoding="utf-8")
        code = "\n".join(line for line in adapter.splitlines() if not line.lstrip().startswith("//"))
        self.assertIn("import { parse, TomlDate } from 'smol-toml';", code)
        self.assertIn("parse(decoder.decode(bytes), { integersAsBigInt: true })", code)
        self.assertEqual(code.count("parse("), 1)
        self.assertIn("new TextDecoder('utf-8', { fatal: true, ignoreBOM: true })", code)
        for forbidden in ("JSON.parse", "eval(", "Function(", "require("):
            self.assertNotIn(forbidden, code)

    def test_coverage_and_feedback_stay_in_package_source(self):
        prefix = "/work/node_modules/smol-toml/"
        self.assertEqual(self.manifest["coverage_subject_prefix"], prefix)
        self.assertGreater(self.receipt["format_specific_source_lines_covered"], 0)
        self.assertLessEqual(self.receipt["format_specific_source_lines_covered"],
                             self.receipt["parser_source_lines_covered"])
        overlay = read(OVERLAY / "verification.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(overlay["base_image_id"], self.receipt["image_id"])
        self.assertIn(f"ENV PARSARIUM_SUBJECT_PREFIX={prefix}\n", (OVERLAY / "Dockerfile").read_text(encoding="utf-8"))
        result, = [item for item in read(BASE / "afl-feedback.json")["results"]
                   if item["project"] == f"toml/javascript/{SLUG}"]
        self.assertEqual(result["overlay_receipt_sha256"], sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(result["control_afl_tuples"], overlay["feedback_edges"])
        self.assertEqual(result["repeats_per_control"], 3)
        self.assertTrue(result["repeated_control_identical"] and result["repeated_differential_identical"])
        self.assertGreaterEqual(result["parser_feature_difference"], 2)
        self.assertGreaterEqual(result["afl_tuple_difference"], 2)
        changed = {**result["control_only_features_by_file"], **result["differential_only_features_by_file"]}
        self.assertTrue(changed and all(name.startswith("dist/") for name in changed))
        self.assertTrue(all(name.startswith("dist/") for name in result["control_parser_source_lines_by_file"]))


if __name__ == "__main__":
    unittest.main()
