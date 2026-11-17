"""pecl/yaml's selected path matches the hand-written YAML typed trees, pinned and with native parser feedback."""

from hashlib import sha256
import json
from pathlib import Path
import runpy
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/yaml"
PROJECT = ROOT / "projects/yaml/php/pecl_yaml"
OVERLAY = ROOT / "fuzzing/afl-native/yaml/php/pecl_yaml"
REPORT = BASE / "pecl-yaml-feedback-differential.json"
PACKAGE = "pecl/yaml"
CHECKS = runpy.run_path(str(ROOT / "controls/yaml/check_controls.py"))
INSTRUMENTED = [
    "pecl-yaml-2.3.0/.libs/detect.o",
    "pecl-yaml-2.3.0/.libs/parse.o",
    "pecl-yaml-2.3.0/.libs/yaml.o",
    "yaml-0.2.5/build/src/.libs/parser.o",
    "yaml-0.2.5/build/src/.libs/reader.o",
    "yaml-0.2.5/build/src/.libs/scanner.o",
]


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def oracle(name: str) -> dict:
    tree = CHECKS["EXPECTED"][name]
    return {**CHECKS["summary"](tree), "tree": tree}


class PhpYamlPeclYamlTest(unittest.TestCase):
    def test_both_typed_trees_match_the_yaml_oracle(self):
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
            self.assertEqual(CHECKS["CONTROLS"][path.name], manifest[hash_key])
            self.assertEqual(manifest[output_key], oracle(path.name))
            self.assertEqual(target["expected_output_by_control_sha256"][manifest[hash_key]], oracle(path.name))
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        self.assertEqual(parser["differential_expected_output"], manifest["differential_expected_output"])
        record, = [item for item in read(BASE / "verification.json")["third_party"] if item["package"] == PACKAGE]
        self.assertTrue(record["pass"])
        self.assertEqual(record["output"], manifest["expected_output"])
        self.assertEqual(record["second_valid_output"], manifest["differential_expected_output"])
        self.assertEqual(record["parser_source_lines_covered"], receipt["parser_source_lines_covered"])

    def test_release_lock_and_adoption_are_pinned(self):
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")
        package = lock[PACKAGE]
        self.assertEqual((parser["version"], manifest["release"], package["release"]), ("2.3.0",) * 3)
        self.assertEqual(manifest["source_sha256"], package["source_sha256"])
        self.assertEqual(manifest["underlying_source_sha256"], lock["libyaml"]["source_sha256"])
        self.assertEqual(manifest["php_source_sha256"], lock["php"]["source_sha256"])
        self.assertEqual(parser["license"], package["license"])
        self.assertIn(package["packagist_source_reference"], parser["license_evidence"])
        dockerfile = (PROJECT / "Dockerfile").read_text()
        overlay_dockerfile = (OVERLAY / "Dockerfile").read_text()
        for text in (dockerfile, overlay_dockerfile):
            self.assertIn(package["archive_url"], text)
            self.assertIn(f"{package['source_sha256']}  /work/parser-source.zip", text)
            self.assertIn(lock["libyaml"]["source_sha256"], text)
            self.assertIn(lock["php"]["source_sha256"], text)
        self.assertIn(package["pecl_archive_url"], dockerfile)
        self.assertIn(package["pecl_archive_sha256"], dockerfile)
        snapshot = read(BASE / "registry-snapshot.json")
        self.assertEqual(snapshot["metrics"][PACKAGE]["value"], parser["popularity"]["value"])
        self.assertGreater(parser["popularity"]["value"], 0)
        self.assertEqual(parser["popularity"]["metric"], "Packagist lifetime downloads")
        self.assertNotIn(PACKAGE, {lead["name"] for lead in read(BASE / "leads.json")})
        ranked = [item["name"] for item in read(BASE / "parsers.json")]
        values = [item["popularity"]["value"] for item in read(BASE / "parsers.json")]
        self.assertEqual(values, sorted(values, reverse=True))
        self.assertLess(ranked.index("symfony/yaml"), ranked.index(PACKAGE))

    def test_native_coverage_and_afl_feedback_are_scoped_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        overlay = read(OVERLAY / "verification.json")
        feedback = read(REPORT)
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(overlay["base_image_id"], receipt["image_id"])
        self.assertEqual(overlay["instrumented_objects"], INSTRUMENTED)
        self.assertEqual(overlay["extension_source_sha256"], manifest["extension_source_sha256"])
        self.assertEqual(overlay["license_file_sha256"], manifest["license_file_sha256"])
        self.assertEqual(overlay["afl_map_size"], 65536)
        self.assertGreaterEqual(overlay["repeats_per_control"], 3)
        self.assertTrue(overlay["all_repeats_identical"])
        self.assertTrue(overlay["full_harness_maps_equal_fuzz_target"])
        self.assertGreater(overlay["afl_tuple_difference"], 0)
        self.assertEqual(overlay["afl_tuple_difference"],
                         overlay["stable_control_only_edges"] + overlay["stable_differential_only_edges"])
        self.assertEqual(overlay["base_coverage_lines"]["control"]["parser_source_lines_covered"],
                         receipt["parser_source_lines_covered"])
        self.assertEqual(feedback["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(feedback["control_afl_tuples"], overlay["feedback_edges"])
        self.assertEqual(feedback["afl_tuple_difference"], overlay["afl_tuple_difference"])
        self.assertEqual(sum(feedback["control_extension_lines_by_file"].values()),
                         receipt["parser_source_lines_covered"])
        self.assertEqual(feedback["control_extension_lines_by_file"]["parse.c"],
                         receipt["format_specific_source_lines_covered"])
        self.assertEqual(sum(feedback["control_libyaml_lines_by_file"].values()),
                         receipt["underlying_source_lines_covered"])
        for name, digest in overlay["overlay_file_sha256"].items():
            self.assertEqual(sha256((OVERLAY / name).read_bytes()).hexdigest(), digest)

    def test_harness_calls_yaml_parse_with_object_maps(self):
        summary = (PROJECT / "summary.php").read_text()
        self.assertIn("yaml_parse($input, 0, $documents, [YAML_MAP_TAG =>", summary)
        self.assertIn("$documents !== 1", summary)
        self.assertIn("parsarium_yaml_parse", (PROJECT / "fuzz-target.php").read_text())
        self.assertIn("src:parsarium-no-php-source.c", (OVERLAY / "Dockerfile").read_text())

    def test_round_two_leads_are_excluded_with_probe_or_source_evidence(self):
        leads = read(BASE / "leads.json")
        probes = {item["package"]: item for item in read(BASE / "round2-lead-probes.json")["probes"]}
        self.assertTrue(all(lead["status"] == "excluded" for lead in leads))
        values = [lead["metric_value"] for lead in leads]
        self.assertEqual(values, sorted(values, reverse=True))
        snapshot = read(BASE / "registry-snapshot.json")
        self.assertEqual([entry["query"] for entry in snapshot["search"]],
                         ["yaml", "yaml parser", "yaml-parser", "yml", "spyc"])
        for lead in leads:
            self.assertEqual(snapshot["metrics"][lead["name"]]["value"], lead["metric_value"])
            if lead.get("evidence") == "data/php/yaml/round2-lead-probes.json":
                self.assertEqual(probes[lead["name"]]["version"], lead["version_probed"])
        for package, probe in probes.items():
            self.assertEqual(set(probe["results"]), {"catalog.yaml", "order.yaml"})
            self.assertEqual(probe["pass"], package == "tbela99/yaml")
        overlap = read(BASE / "round2-lead-probes.json")["tbela99_overlap"]
        self.assertGreater(overlap["shared_with"]["symfony/yaml v5.1.0 (codeload tag archive)"]["shared_lines"],
                           overlap["fork_distinct_lines"] * 3 // 4)


if __name__ == "__main__":
    unittest.main()
