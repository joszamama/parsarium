"""flow-php/postgresql matches the SQL oracle, is pinned, and has native plus package-line feedback."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/sql"
PROJECT = ROOT / "projects/sql/php/flow_php_postgresql"
OVERLAY = ROOT / "fuzzing/afl-native/sql/php/flow_php_postgresql"
EXTENSION = ROOT / "projects/sql/php/flow_php_pg_query_ext"
PACKAGE = "flow-php/postgresql"


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class PhpSqlFlowPostgresqlTest(unittest.TestCase):
    def test_both_summaries_match_the_sql_oracle(self):
        oracle = read(ROOT / "controls/sql/expected.json")["controls"]
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        target = read(PROJECT / "target.json")
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        for control_key, hash_key, output_key in (
                ("control", "control_sha256", "expected_output"),
                ("differential_control", "differential_control_sha256", "differential_expected_output")):
            path = ROOT / manifest[control_key]
            self.assertEqual(sha256(path.read_bytes()).hexdigest(), manifest[hash_key])
            self.assertEqual(manifest[output_key], oracle[path.name])
            self.assertEqual(target["expected_output_by_control_sha256"][manifest[hash_key]], oracle[path.name])
        record, = [item for item in read(BASE / "verification.json")["third_party"] if item["package"] == PACKAGE]
        self.assertTrue(record["pass"])
        self.assertEqual(record["differential_output"], manifest["differential_expected_output"])
        self.assertEqual(record["parser_source_lines_covered"], receipt["parser_source_lines_covered"])

    def test_release_lock_and_shared_native_build_are_pinned(self):
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")
        extension_lock = read(EXTENSION / "source-lock.json")
        self.assertEqual((parser["version"], manifest["release"], lock[PACKAGE]["release"]), ("0.48.0",) * 3)
        composer = read(PROJECT / "composer.lock")
        locked = {item["name"]: item["source"]["reference"] for item in composer["packages"]}
        self.assertEqual(locked[PACKAGE], lock[PACKAGE]["composer_reference"])
        self.assertEqual(locked["google/protobuf"], lock["google/protobuf"]["composer_reference"])
        self.assertEqual(lock["flow-php/pg-query-ext"]["source_sha256"],
                         extension_lock["flow-php/pg-query-ext"]["source_sha256"])
        for field in ("release", "source_sha256", "archive_url"):
            self.assertEqual(lock["libpg_query"][field], extension_lock["libpg_query"][field])
        self.assertEqual(manifest["extension_source_sha256"], read(EXTENSION / "manifest.json")["extension_source_sha256"])
        for text in ((PROJECT / "Dockerfile").read_text(), (OVERLAY / "Dockerfile").read_text()):
            self.assertIn(lock["flow-php/pg-query-ext"]["source_sha256"], text)
            self.assertIn(lock["libpg_query"]["source_sha256"], text)
            self.assertIn("--enable-ctype", text)
        self.assertIn(lock[PACKAGE]["source_sha256"], (PROJECT / "Dockerfile").read_text())
        snapshot = read(BASE / "registry-snapshot.json")
        self.assertEqual(snapshot["metric"]["leads"][PACKAGE]["value"], parser["popularity"]["value"])
        names = [item["name"] for item in read(BASE / "parsers.json")]
        self.assertLess(names.index(PACKAGE), names.index("flow-php/pg-query-ext"))

    def test_native_and_package_feedback_differ_between_controls(self):
        receipt = read(PROJECT / "verification.json")
        overlay = read(OVERLAY / "verification.json")
        differential = read(OVERLAY / "differential.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(overlay["afl_map_size"], 65536)
        self.assertTrue(overlay["all_repeats_identical"] and overlay["full_harness_maps_equal_fuzz_target"])
        self.assertGreater(overlay["afl_tuple_difference"], 0)
        self.assertEqual(differential["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertGreater(differential["parser_feature_difference"], 0)
        self.assertTrue(differential["repeat_features_identical"])
        self.assertGreater(receipt["parser_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        for name, digest in overlay["overlay_file_sha256"].items():
            self.assertEqual(sha256((OVERLAY / name).read_bytes()).hexdigest(), digest)

    def test_harness_uses_the_documented_dsl_and_package_traverser(self):
        summary = (PROJECT / "summary.php").read_text()
        self.assertIn("return sql_parse($sql);", summary)
        self.assertIn("implements NodeVisitor", summary)
        self.assertIn("$query->traverse($visitor);", summary)
        self.assertNotIn("pg_query_parse(", summary)


if __name__ == "__main__":
    unittest.main()
