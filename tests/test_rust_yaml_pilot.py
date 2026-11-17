"""Check the Rust YAML pilot paths against the typed-tree oracle and their scoped AFL++ evidence."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
CELL = ROOT / "data/rust/yaml"
SLUGS = {
    "serde_yaml": "serde_yaml",
    "yaml-rust": "yaml_rust",
    "unsafe-libyaml": "unsafe_libyaml",
    "yaml-rust2": "yaml_rust2",
    "serde-saphyr": "serde_saphyr",
    "granit-parser": "granit_parser",
    "saphyr-parser": "saphyr_parser",
    "saphyr": "saphyr",
    "noyalib": "noyalib",
    "dbt-yaml": "dbt_yaml",
}
CRATES = {
    "serde_yaml": ["serde_yaml", "unsafe_libyaml"],
    "yaml-rust": ["yaml_rust"],
    "unsafe-libyaml": ["unsafe_libyaml"],
    "yaml-rust2": ["yaml_rust2"],
    "serde-saphyr": ["granit_parser", "serde_saphyr"],
    "granit-parser": ["granit_parser", "parsarium_yaml_granit_parser_events"],
    "saphyr-parser": ["parsarium_yaml_saphyr_parser_events", "saphyr_parser"],
    "saphyr": ["parsarium_yaml_saphyr_events", "saphyr", "saphyr_parser"],
    "noyalib": ["noyalib"],
    "dbt-yaml": ["dbt_yaml", "unsafe_libyaml"],
}
spec = importlib.util.spec_from_file_location("yaml_control_oracle", ROOT / "controls/yaml/check_controls.py")
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)


def selected() -> list[str]:
    return [parser["name"] for parser in json.loads((CELL / "parsers.json").read_text())]


class RustYamlPilotTest(unittest.TestCase):
    def test_controls_match_hand_written_typed_trees(self):
        for name in selected():
            with self.subTest(name=name):
                manifest = json.loads((ROOT / "projects/yaml/rust" / SLUGS[name] / "manifest.json").read_text())
                for path_key, digest_key, output_key in (
                        ("control", "control_sha256", "expected_output"),
                        ("afl_variant", "afl_variant_sha256", "afl_variant_expected_output")):
                    path = ROOT / manifest[path_key]
                    self.assertEqual(sha256(path.read_bytes()).hexdigest(), manifest[digest_key])
                    self.assertEqual(manifest[output_key], {"tree": oracle.EXPECTED[path.name]})
                receipt = json.loads((ROOT / "projects/yaml/rust" / SLUGS[name] / "verification.json").read_text())
                self.assertTrue(receipt["pass"])
                self.assertEqual(receipt["output"], manifest["expected_output"])
                self.assertGreater(receipt["parser_source_lines_covered"], 0)

    def test_source_pins_and_scoped_stable_feedback(self):
        for name in selected():
            with self.subTest(name=name):
                project = ROOT / "projects/yaml/rust" / SLUGS[name]
                manifest = json.loads((project / "manifest.json").read_text())
                lock = tomllib.loads((project / "Cargo.lock").read_text())
                pins = {(item["name"], item["version"]): item.get("checksum") for item in lock["package"]}
                self.assertEqual(pins[(manifest["package"], manifest["release"])], manifest["source_sha256"])
                if "underlying_package" in manifest:
                    self.assertEqual(pins[(manifest["underlying_package"], manifest["underlying_release"])],
                                     manifest["underlying_source_sha256"])
                feedback = json.loads((ROOT / "fuzzing/afl-native/yaml/rust" / SLUGS[name] /
                                       "verification.json").read_text())
                self.assertEqual(manifest["afl_instrumented_crates"], CRATES[name])
                self.assertEqual(set(feedback["sancov_scope"]["rlib_guard_bytes"]), set(CRATES[name]))
                self.assertGreaterEqual(feedback["repeats"], 3)
                self.assertTrue(feedback["control_stability"]["all_repeats_identical"])
                self.assertTrue(feedback["variant_stability"]["all_repeats_identical"])
                self.assertGreater(feedback["edges_only_in_control"] + feedback["edges_only_in_variant"], 0)
                self.assertTrue(feedback["source_differential"]["files_with_different_line_counts"])
                self.assertEqual(feedback["control_output"], manifest["expected_output"])
                self.assertEqual(feedback["variant_output"], manifest["afl_variant_expected_output"])

    def test_cell_ranks_selected_paths_and_records_family(self):
        cell = json.loads((CELL / "cell.json").read_text())
        parsers = json.loads((CELL / "parsers.json").read_text())
        leads = {lead["name"]: lead for lead in json.loads((CELL / "leads.json").read_text())}
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        values = [parser["metric"]["value"] for parser in parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        for parser in parsers:
            self.assertEqual(leads[parser["name"]]["status"], "selected")
            self.assertEqual(leads[parser["name"]]["metric_value"], parser["metric"]["value"])
        families = {parser["name"]: parser["family"] for parser in parsers}
        for name in ("serde_yaml", "unsafe-libyaml"):
            if name in families:
                self.assertIn("libyaml", families[name])
        for name in set(families) - {"serde_yaml", "unsafe-libyaml", "yaml-rust", "noyalib", "dbt-yaml"}:
            self.assertIn("yaml-rust lineage", families[name])


if __name__ == "__main__":
    unittest.main()
