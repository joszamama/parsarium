"""symfony/yaml's selected path matches the hand-written YAML typed trees, pinned and with parser feedback."""

from hashlib import sha256
import json
from pathlib import Path
import runpy
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/yaml"
PROJECT = ROOT / "projects/yaml/php/symfony_yaml"
OVERLAY = ROOT / "fuzzing/afl-native/yaml/php/symfony_yaml"
REPORT = BASE / "symfony-yaml-feedback-differential.json"
PACKAGE = "symfony/yaml"
SOURCE = "/work/vendor/symfony/yaml/"
CHECKS = runpy.run_path(str(ROOT / "controls/yaml/check_controls.py"))


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def oracle(name: str) -> dict:
    tree = CHECKS["EXPECTED"][name]
    return {**CHECKS["summary"](tree), "tree": tree}


class PhpYamlSymfonyYamlTest(unittest.TestCase):
    def test_both_typed_trees_match_the_yaml_oracle(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        target = read(PROJECT / "target.json")
        feedback = read(REPORT)
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        for control_key, hash_key, output_key in (
                ("control", "control_sha256", "expected_output"),
                ("differential_control", "differential_control_sha256", "differential_expected_output")):
            path = ROOT / manifest[control_key]
            self.assertEqual(sha256(path.read_bytes()).hexdigest(), manifest[hash_key])
            self.assertEqual(CHECKS["CONTROLS"][path.name], manifest[hash_key])
            self.assertEqual(manifest[output_key], oracle(path.name))
            self.assertEqual(target["expected_output_by_control_sha256"][manifest[hash_key]], oracle(path.name))
        self.assertTrue(feedback["control_output_matches_oracle"])
        self.assertTrue(feedback["differential_output_matches_oracle"])
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        record, = [item for item in read(BASE / "verification.json")["third_party"] if item["package"] == PACKAGE]
        self.assertEqual(record["output"], manifest["expected_output"])
        self.assertEqual(record["second_valid_output"], manifest["differential_expected_output"])

    def test_release_lock_and_adoption_are_pinned(self):
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        composer, = [item for item in read(PROJECT / "composer.lock")["packages"] if item["name"] == PACKAGE]
        self.assertEqual((parser["version"], manifest["release"], composer["version"]), (lock["release"],) * 3)
        self.assertEqual(composer["source"]["reference"], lock["composer_reference"])
        self.assertEqual(composer["dist"]["reference"], lock["composer_reference"])
        self.assertEqual(composer["license"], ["MIT"])
        self.assertEqual(parser["license"], "MIT")
        self.assertIn(lock["composer_reference"], parser["license_evidence"])
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertIn(lock["archive_url"], dockerfile)
        self.assertIn(f"{lock['source_sha256']}  /work/parser-source.zip", dockerfile)
        self.assertIn("diff -r /work/parser-source/symfony-yaml-e8266f5 /work/vendor/symfony/yaml", dockerfile)
        snapshot = read(BASE / "registry-snapshot.json")
        self.assertEqual(snapshot["metrics"][PACKAGE]["value"], parser["popularity"]["value"])
        self.assertEqual(parser["popularity"]["metric"], "Packagist lifetime downloads")
        self.assertNotIn(PACKAGE, {lead["name"] for lead in read(BASE / "leads.json")})

    def test_coverage_and_afl_feedback_are_parser_scoped_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        overlay = read(OVERLAY / "verification.json")
        feedback = read(REPORT)
        self.assertEqual(manifest["coverage_subject_prefix"], SOURCE)
        self.assertIn(f"ENV PARSARIUM_SUBJECT_PREFIX={SOURCE}\n", (OVERLAY / "Dockerfile").read_text())
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(overlay["base_image_id"], receipt["image_id"])
        self.assertEqual(feedback["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(sum(feedback["control_source_lines_by_file"].values()),
                         receipt["parser_source_lines_covered"])
        self.assertEqual(feedback["control_source_lines_by_file"]["Parser.php"],
                         receipt["format_specific_source_lines_covered"])
        self.assertEqual(feedback["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(feedback["control_afl_tuples"], overlay["feedback_edges"])
        self.assertEqual(feedback["runs_per_control"], 3)
        self.assertTrue(feedback["repeated_control_identical"])
        self.assertTrue(feedback["repeated_differential_identical"])
        self.assertGreater(feedback["parser_feature_difference"], 0)
        self.assertGreater(feedback["afl_tuple_difference"], 0)
        self.assertEqual(sum(feedback["control_only_features_by_file"].values()) +
                         sum(feedback["differential_only_features_by_file"].values()),
                         feedback["parser_feature_difference"])

    def test_harness_calls_the_package_parser_with_object_maps(self):
        harness = (PROJECT / "harness.php").read_text()
        self.assertIn("Yaml::parse($input, Yaml::PARSE_OBJECT_FOR_MAP)", harness)
        self.assertNotIn("yaml_parse(", harness)
        self.assertIn("parsarium_parse", (PROJECT / "fuzz-target.php").read_text())

    def test_spyc_stays_an_excluded_lead_with_probe_evidence(self):
        lead, = [item for item in read(BASE / "leads.json") if item["name"] == "mustangostang/spyc"]
        probe = read(BASE / "spyc-valid-control-probe.json")
        self.assertEqual(lead["status"], "excluded")
        self.assertFalse(probe["pass"])
        observed = probe["observed_output"]["catalog.yaml"]
        self.assertNotEqual(observed["title"], CHECKS["EXPECTED"]["catalog.yaml"][1][7][1][1])
        self.assertEqual(observed["items"][0]["note"], "line one\nline two")


if __name__ == "__main__":
    unittest.main()
