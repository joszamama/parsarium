"""internal/toml's selected path matches both hand-written TOML typed trees with stable parser feedback."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/toml"
SLUG = "internal_toml"
PROJECT = ROOT / "projects/toml/php" / SLUG
OVERLAY = ROOT / "fuzzing/afl-native/toml/php" / SLUG
REPORT = BASE / "internal-toml-feedback-differential.json"
PACKAGE = "internal/toml"
LICENSE = "BSD-3-Clause"
SOURCE = "/work/vendor/internal/toml/"
ENTRY = "Toml::parse($input)"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class PhpTomlInternalTomlTest(unittest.TestCase):
    def test_both_typed_trees_match_the_control_oracles(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        feedback = read(REPORT)
        target = read(PROJECT / "target.json")
        self.assertEqual((manifest["format"], manifest["ecosystem"], manifest["package"]), ("toml", "php", PACKAGE))
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        self.assertTrue(feedback["control_output_matches_oracle"])
        self.assertTrue(feedback["differential_output_matches_oracle"])
        for control_key, hash_key, output_key in (
                ("control", "control_sha256", "expected_output"),
                ("differential_control", "differential_control_sha256", "differential_expected_output")):
            control = ROOT / manifest[control_key]
            self.assertEqual(sha256(control.read_bytes()).hexdigest(), manifest[hash_key])
            oracle = read(control.with_name(control.stem + ".expected.json"))
            self.assertEqual(manifest[output_key], oracle)
            self.assertEqual(target["expected_output_by_control_sha256"][manifest[hash_key]], oracle)
        self.assertEqual(manifest["control"], "controls/toml/service-config.toml")
        self.assertEqual(manifest["differential_control"], "controls/toml/typed-scalars.toml")
        self.assertEqual(set(target["expected_output_by_control_sha256"]),
                         {manifest["control_sha256"], manifest["differential_control_sha256"]})
        record, = [item for item in read(BASE / "verification.json")["third_party"] if item["package"] == PACKAGE]
        self.assertTrue(record["pass"])
        self.assertEqual(record["output"], manifest["expected_output"])
        self.assertEqual(record["second_valid_output"], manifest["differential_expected_output"])

    def test_release_lock_license_and_adoption_are_pinned(self):
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        composer, = [item for item in read(PROJECT / "composer.lock")["packages"] if item["name"] == PACKAGE]
        self.assertEqual((parser["version"], manifest["release"], composer["version"]), (lock["release"],) * 3)
        self.assertEqual(composer["source"]["reference"], lock["composer_reference"])
        self.assertEqual(composer["dist"]["reference"], lock["composer_reference"])
        self.assertEqual(composer["license"], [LICENSE])
        self.assertEqual(parser["license"], LICENSE)
        self.assertIn(lock["composer_reference"], parser["license_evidence"])
        self.assertIn(lock["composer_reference"], parser["documentation"])
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertIn(lock["archive_url"], dockerfile)
        self.assertIn(f"{lock['source_sha256']}  /work/parser-source.zip", dockerfile)
        self.assertIn("diff -r", dockerfile)
        self.assertIn(manifest["base_image"], dockerfile)
        snapshot = read(BASE / "registry-snapshot.json")
        hits = {hit["downloads_lifetime"] for query in snapshot["search"]
                for hit in query["hits"] if hit["name"] == PACKAGE}
        self.assertEqual(hits, {parser["metric"]["value"]})
        self.assertEqual(parser["metric"]["captured_at_utc"], snapshot["captured_at_utc"])
        self.assertEqual(parser["metric"]["name"], "Packagist total downloads")
        self.assertNotIn(PACKAGE, {lead["name"] for lead in read(BASE / "leads.json")["leads"]})
        self.assertIn(f"projects/toml/php/{SLUG}/verification.json",
                      {item["project_receipt"] for item in read(BASE / "cell.json")["third_party_control_results"]})

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
        self.assertEqual(overlay["control_sha256"], manifest["control_sha256"])
        self.assertEqual(feedback["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(sum(feedback["control_source_lines_by_file"].values()),
                         receipt["parser_source_lines_covered"])
        self.assertEqual(sum(feedback["differential_source_lines_by_file"].values()),
                         feedback["differential_parser_source_lines"])
        suffix = manifest["format_specific_coverage_file_suffix"].removeprefix("/")
        self.assertEqual(feedback["control_source_lines_by_file"][suffix],
                         receipt["format_specific_source_lines_covered"])
        self.assertEqual(feedback["control_parser_features"], receipt["parser_source_lines_covered"])
        self.assertEqual(feedback["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(feedback["control_afl_tuples"], overlay["feedback_edges"])
        self.assertGreaterEqual(feedback["repeats_per_control"], 3)
        self.assertTrue(feedback["repeated_control_identical"])
        self.assertTrue(feedback["repeated_differential_identical"])
        self.assertGreaterEqual(feedback["parser_feature_difference"], 2)
        self.assertGreaterEqual(feedback["afl_tuple_difference"], 2)
        self.assertEqual(sum(feedback["control_only_features_by_file"].values()) +
                         sum(feedback["differential_only_features_by_file"].values()),
                         feedback["parser_feature_difference"])
        row, = [item for item in read(BASE / "afl-feedback.json")["results"]
                if item["project"] == f"toml/php/{SLUG}"]
        self.assertEqual(row["afl_tuple_difference"], feedback["afl_tuple_difference"])
        self.assertEqual(row["overlay_receipt_sha256"], feedback["overlay_receipt_sha256"])

    def test_harness_builds_the_tree_from_the_library_not_the_text(self):
        harness = (PROJECT / "harness.php").read_text()
        self.assertIn(ENTRY, harness)
        self.assertNotIn("preg_match('/^\\d", harness)
        self.assertIn("serialize(parsarium_project($nodes))", harness)
        self.assertIn("parsarium_parse", (PROJECT / "fuzz-target.php").read_text())


if __name__ == "__main__":
    unittest.main()
