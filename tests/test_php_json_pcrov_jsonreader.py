"""pcrov/jsonreader's selected scope matches independent valid-control JSON trees."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/json"
PROJECT = ROOT / "projects/json/php/pcrov_jsonreader"
OVERLAY = ROOT / "fuzzing/afl-native/json/php/pcrov_jsonreader"
SOURCE = "/work/vendor/pcrov/jsonreader/"


def read(path: Path) -> dict:
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
    return {"type": "object", "members": {key: type_tag(value[key]) for key in sorted(value)}}


class PhpJsonPcrovJsonReaderTest(unittest.TestCase):
    def test_both_type_tagged_trees_match_python_json_oracle(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        feedback = read(BASE / "pcrov-jsonreader-feedback-differential.json")
        target = read(PROJECT / "target.json")
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        self.assertTrue(feedback["control_output_matches_oracle"])
        self.assertTrue(feedback["differential_output_matches_oracle"])
        self.assertTrue(feedback["file_and_stream_api_match"])
        for control_key, hash_key, output_key in (
                ("control", "control_sha256", "expected_output"),
                ("differential_control", "differential_control_sha256",
                 "differential_expected_output")):
            data = (ROOT / manifest[control_key]).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), manifest[hash_key])
            oracle = type_tag(json.loads(data.decode("utf-8"), object_pairs_hook=unique_members))
            self.assertEqual(oracle, manifest[output_key])
            self.assertEqual(target["expected_output_by_control_sha256"][manifest[hash_key]], oracle)
        self.assertEqual(set(target["expected_output_by_control_sha256"]),
                         {manifest["control_sha256"], manifest["differential_control_sha256"]})

    def test_release_lock_and_adoption_are_pinned(self):
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "pcrov/jsonreader"]
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")["pcrov/jsonreader"]
        composer, = [item for item in read(PROJECT / "composer.lock")["packages"]
                     if item["name"] == "pcrov/jsonreader"]
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
                for hit in query["hits"]
                if hit["name"] == "pcrov/jsonreader"}
        self.assertEqual(hits, {parser["popularity"]["value"]})
        self.assertEqual(parser["popularity"]["captured_at_utc"], snapshot["captured_at_utc"])
        self.assertEqual(parser["popularity"]["metric"], "Packagist total downloads")
        self.assertNotIn("pcrov/jsonreader", {lead["name"] for lead in read(BASE / "leads.json")})

    def test_coverage_and_afl_feedback_are_parser_scoped_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        overlay = read(OVERLAY / "verification.json")
        feedback = read(BASE / "pcrov-jsonreader-feedback-differential.json")
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
        parser_files = {"src/Parser/JsonParser.php", "src/Parser/Lexer.php", "src/JsonReader.php"}
        for key in ("control_only_features_by_file", "differential_only_features_by_file"):
            self.assertLessEqual(set(feedback[key]), parser_files)
        self.assertEqual(sum(feedback["control_only_features_by_file"].values()) +
                         sum(feedback["differential_only_features_by_file"].values()),
                         feedback["parser_feature_difference"])

    def test_package_source_has_no_ext_json_route_in_harness(self):
        harness = (PROJECT / "harness.php").read_text()
        self.assertIn("$reader->json($input)", harness)
        self.assertNotIn("json_decode", harness)
        self.assertIn("parsarium_parse", (PROJECT / "fuzz-target.php").read_text())


if __name__ == "__main__":
    unittest.main()
