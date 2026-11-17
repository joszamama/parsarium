"""boundwize/jsonrecast's selected scope matches independent valid-control JSON trees in order."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/json"
PROJECT = ROOT / "projects/json/php/boundwize_jsonrecast"
OVERLAY = ROOT / "fuzzing/afl-native/json/php/boundwize_jsonrecast"
REPORT = BASE / "boundwize-jsonrecast-feedback-differential.json"
PACKAGE = "boundwize/jsonrecast"
SOURCE = "/work/vendor/boundwize/jsonrecast/"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def unique_members(pairs: list) -> dict:
    if len({key for key, _ in pairs}) != len(pairs):
        raise ValueError("duplicate key in control")
    return dict(pairs)


def type_tag(value: object) -> dict:
    if value is None:
        return {"type": "null"}
    if isinstance(value, bool):
        return {"type": "boolean", "value": value}
    if isinstance(value, (int, float)):
        return {"type": "number", "value": value}
    if isinstance(value, str):
        return {"type": "string", "value": value}
    if isinstance(value, list):
        return {"type": "array", "items": [type_tag(item) for item in value]}
    return {"type": "object", "members": {key: type_tag(item) for key, item in value.items()}}


def ordered(tree: object) -> str:
    """Serialization that keeps member order and distinguishes 1 from 1.0."""
    return json.dumps(tree, ensure_ascii=False)


class PhpJsonBoundwizeJsonRecastTest(unittest.TestCase):
    def test_both_type_tagged_trees_match_python_json_oracle_in_order(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        feedback = read(REPORT)
        target = read(PROJECT / "target.json")
        self.assertTrue(receipt["pass"])
        self.assertEqual(ordered(receipt["output"]), ordered(manifest["expected_output"]))
        self.assertTrue(feedback["control_output_matches_oracle"])
        self.assertTrue(feedback["differential_output_matches_oracle"])
        self.assertTrue(feedback["ordered_members_and_number_kinds_checked"])
        for control_key, hash_key, output_key in (
                ("control", "control_sha256", "expected_output"),
                ("differential_control", "differential_control_sha256",
                 "differential_expected_output")):
            data = (ROOT / manifest[control_key]).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), manifest[hash_key])
            oracle = type_tag(json.loads(data.decode("utf-8"), object_pairs_hook=unique_members))
            self.assertEqual(ordered(oracle), ordered(manifest[output_key]))
            self.assertEqual(ordered(target["expected_output_by_control_sha256"][manifest[hash_key]]),
                             ordered(oracle))
        self.assertEqual(set(target["expected_output_by_control_sha256"]),
                         {manifest["control_sha256"], manifest["differential_control_sha256"]})
        verification, = [item for item in read(BASE / "verification.json")["third_party"]
                         if item["package"] == PACKAGE]
        self.assertEqual(verification["output"], manifest["expected_output"])
        self.assertEqual(verification["second_valid_output"], manifest["differential_expected_output"])

    def test_release_lock_and_adoption_are_pinned(self):
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        composer, = [item for item in read(PROJECT / "composer.lock")["packages"]
                     if item["name"] == PACKAGE]
        self.assertEqual((parser["version"], manifest["release"], composer["version"]),
                         (lock["release"],) * 3)
        self.assertEqual(composer["source"]["reference"], lock["composer_reference"])
        self.assertEqual(composer["dist"]["reference"], lock["composer_reference"])
        self.assertEqual(composer["license"], ["MIT"])
        self.assertEqual(parser["license"], "MIT")
        self.assertIn(lock["composer_reference"], parser["license_evidence"])
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertIn(lock["archive_url"], dockerfile)
        self.assertIn(f"{lock['source_sha256']}  /work/parser-source.zip", dockerfile)
        self.assertIn("diff -r", dockerfile)
        snapshot = read(BASE / "registry-snapshot.json")
        hits = {hit["downloads"] for query in snapshot["search"]
                for hit in query["hits"] if hit["name"] == PACKAGE}
        self.assertEqual(hits, {parser["popularity"]["value"]})
        self.assertEqual(parser["popularity"]["captured_at_utc"], snapshot["captured_at_utc"])
        self.assertEqual(parser["popularity"]["metric"], "Packagist total downloads")
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
        self.assertEqual(feedback["control_source_lines_by_file"]["src/Parser/Lexer.php"],
                         receipt["format_specific_source_lines_covered"])
        self.assertEqual(feedback["control_parser_features"], receipt["parser_source_lines_covered"])
        self.assertEqual(feedback["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(feedback["control_afl_tuples"], overlay["feedback_edges"])
        self.assertTrue(feedback["repeated_control_identical"])
        self.assertTrue(feedback["repeated_differential_identical"])
        self.assertGreater(feedback["parser_feature_difference"], 0)
        self.assertGreater(feedback["afl_tuple_difference"], 0)
        self.assertEqual(sum(feedback["control_only_features_by_file"].values()) +
                         sum(feedback["differential_only_features_by_file"].values()),
                         feedback["parser_feature_difference"])
        cell_feedback, = [item for item in read(BASE / "afl-feedback.json")["results"]
                          if item["project"] == "json/php/boundwize_jsonrecast"]
        self.assertEqual(cell_feedback["afl_tuple_difference"], feedback["afl_tuple_difference"])
        self.assertEqual(cell_feedback["overlay_receipt_sha256"], feedback["overlay_receipt_sha256"])

    def test_harness_calls_the_package_parser_not_ext_json(self):
        harness = (PROJECT / "harness.php").read_text()
        self.assertIn("JsonRecast::parse($input)", harness)
        self.assertNotIn("json_decode", harness)
        self.assertIn("parsarium_parse", (PROJECT / "fuzz-target.php").read_text())


if __name__ == "__main__":
    unittest.main()
