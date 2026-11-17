"""flow-php/pg-query-ext matches the SQL oracle, is pinned, and has scoped native libpg_query feedback."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/sql"
PROJECT = ROOT / "projects/sql/php/flow_php_pg_query_ext"
OVERLAY = ROOT / "fuzzing/afl-native/sql/php/flow_php_pg_query_ext"
PACKAGE = "flow-php/pg-query-ext"
INSTRUMENTED = [
    "libpg_query-18.0.0/src/postgres/src_backend_parser_gram.o",
    "libpg_query-18.0.0/src/postgres/src_backend_parser_parser.o",
    "libpg_query-18.0.0/src/postgres/src_backend_parser_scan.o",
    "pg-query-ext-0.48.0/ext/.libs/pg_query.o",
]


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class PhpSqlFlowPgQueryExtTest(unittest.TestCase):
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
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        self.assertEqual(parser["differential_expected_output"], manifest["differential_expected_output"])
        record, = [item for item in read(BASE / "verification.json")["third_party"] if item["package"] == PACKAGE]
        self.assertTrue(record["pass"])
        self.assertEqual(record["output"], manifest["expected_output"])
        self.assertEqual(record["differential_output"], manifest["differential_expected_output"])
        self.assertEqual(record["parser_source_lines_covered"], receipt["parser_source_lines_covered"])
        self.assertEqual(record["underlying_source_lines_covered"], receipt["underlying_source_lines_covered"])

    def test_release_lock_licence_and_adoption_are_pinned(self):
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")
        package = lock[PACKAGE]
        self.assertEqual((parser["version"], manifest["release"], package["release"]), ("0.48.0",) * 3)
        self.assertEqual(manifest["source_sha256"], package["source_sha256"])
        self.assertEqual(manifest["underlying_source_sha256"], lock["libpg_query"]["source_sha256"])
        self.assertEqual(manifest["php_source_sha256"], lock["php"]["source_sha256"])
        self.assertIn(package["license_file_sha256"], parser["license_evidence"])
        self.assertEqual(manifest["license_file_sha256"]["pg-query-ext-0.48.0/LICENSE.flow-monorepo"],
                         package["license_file_sha256"])
        for text in ((PROJECT / "Dockerfile").read_text(), (OVERLAY / "Dockerfile").read_text()):
            self.assertIn(package["archive_url"], text)
            self.assertIn(f"{package['source_sha256']}  /work/parser-source.tar.gz", text)
            self.assertIn(package["license_file_url"], text)
            self.assertIn(lock["libpg_query"]["source_sha256"], text)
            self.assertIn(lock["php"]["source_sha256"], text)
        snapshot = read(BASE / "registry-snapshot.json")
        self.assertEqual(snapshot["metric"]["leads"][PACKAGE]["value"], parser["popularity"]["value"])
        values = [item["popularity"]["value"] for item in read(BASE / "parsers.json")]
        self.assertEqual(values, sorted(values, reverse=True))
        lead, = [item for item in read(BASE / "leads.json")["leads"] if item["name"] == PACKAGE]
        self.assertEqual((lead["status"], lead["selected_release"]), ("selected", "0.48.0"))

    def test_native_coverage_and_afl_feedback_are_scoped_and_differential(self):
        receipt = read(PROJECT / "verification.json")
        overlay = read(OVERLAY / "verification.json")
        differential = read(OVERLAY / "differential.json")
        manifest = read(PROJECT / "manifest.json")
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(overlay["base_image_id"], receipt["image_id"])
        self.assertEqual(overlay["instrumented_objects"], INSTRUMENTED)
        self.assertEqual(overlay["extension_source_sha256"], manifest["extension_source_sha256"])
        self.assertEqual(overlay["license_file_sha256"], manifest["license_file_sha256"])
        self.assertEqual(overlay["afl_map_size"], 65536)
        self.assertTrue(overlay["all_repeats_identical"] and overlay["full_harness_maps_equal_fuzz_target"])
        self.assertEqual(overlay["afl_tuple_difference"],
                         overlay["stable_control_only_edges"] + overlay["stable_differential_only_edges"])
        self.assertEqual(overlay["base_coverage_lines"]["control"]["parser_source_lines_covered"],
                         receipt["parser_source_lines_covered"])
        self.assertEqual(differential["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(differential["first_afl_tuples"], overlay["feedback_edges"])
        self.assertEqual(differential["afl_tuple_difference"], overlay["afl_tuple_difference"])
        for name, digest in overlay["overlay_file_sha256"].items():
            self.assertEqual(sha256((OVERLAY / name).read_bytes()).hexdigest(), digest)

    def test_harness_calls_pg_query_parse_only(self):
        summary = (PROJECT / "summary.php").read_text()
        self.assertIn("return pg_query_parse($sql);", summary)
        self.assertNotIn("pg_query_parse_protobuf", summary)
        self.assertIn("src:parsarium-no-php-source.c", (OVERLAY / "Dockerfile").read_text())
        self.assertTrue((PROJECT / "fuzz-target.php").read_text().startswith("#!/opt/php/bin/php\n"))


if __name__ == "__main__":
    unittest.main()
