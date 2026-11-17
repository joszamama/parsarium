"""Check the taplo crate's TOML controls, independent family and scoped AFL++ evidence."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
SLUG, PACKAGE, OWN_CRATE = "taplo", "taplo", "taplo"
PROJECT = ROOT / "projects/toml/rust" / SLUG
OVERLAY = ROOT / "fuzzing/afl-native/toml/rust" / SLUG
MANIFEST = json.loads((PROJECT / "manifest.json").read_text())
spec = importlib.util.spec_from_file_location("toml_control_oracle", ROOT / "controls/toml/check_controls.py")
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)


class TaploCrateEvidenceTest(unittest.TestCase):
    def test_controls_match_tomllib_oracle_and_expected_trees(self):
        for path_key, digest_key, output_key, expected_file in (
            ("control", "control_sha256", "expected_output", "service-config.expected.json"),
            ("afl_variant", "afl_variant_sha256", "afl_variant_expected_output", "typed-scalars.expected.json"),
        ):
            data = (ROOT / MANIFEST[path_key]).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), MANIFEST[digest_key])
            self.assertEqual(oracle.typed(tomllib.loads(data.decode())), MANIFEST[output_key])
            self.assertEqual(json.loads((ROOT / "controls/toml" / expected_file).read_text()),
                             MANIFEST[output_key])
        self.assertEqual(MANIFEST["control"], "controls/toml/service-config.toml")
        self.assertEqual(MANIFEST["afl_variant"], "controls/toml/typed-scalars.toml")

    def test_source_pins_receipt_and_independent_family(self):
        lock = tomllib.loads((PROJECT / "Cargo.lock").read_text())
        pins = {(package["name"], package["version"]): package.get("checksum") for package in lock["package"]}
        self.assertEqual(pins[(PACKAGE, MANIFEST["release"])], MANIFEST["source_sha256"])
        names = {package["name"] for package in lock["package"]}
        for other in ("toml", "toml_parser", "toml_edit", "basic-toml", "toml-span"):
            self.assertNotIn(other, names)
        source_lock = json.loads((PROJECT / "source-lock.json").read_text())
        self.assertEqual(source_lock[PACKAGE]["source_sha256"], MANIFEST["source_sha256"])
        self.assertEqual(source_lock[PACKAGE]["release"], MANIFEST["release"])
        dockerfile = (PROJECT / "Dockerfile").read_text()
        for digest in (MANIFEST["source_sha256"], MANIFEST["base_image"], MANIFEST["runtime_base_image"]):
            self.assertIn(digest, dockerfile)
        self.assertTrue(MANIFEST["coverage_subject_prefix"].endswith(f"/{PACKAGE}-{MANIFEST['release']}/"))
        self.assertNotIn("underlying_coverage_subject_prefix", MANIFEST)
        receipt = json.loads((PROJECT / "verification.json").read_text())
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], MANIFEST["expected_output"])
        self.assertEqual(receipt["source_sha256"], MANIFEST["source_sha256"])
        self.assertEqual(receipt["control_sha256"], MANIFEST["control_sha256"])
        self.assertGreater(receipt["parser_source_lines_covered"], 0)
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        current = {str(path.relative_to(PROJECT)): sha256(path.read_bytes()).hexdigest()
                   for path in sorted(PROJECT.rglob("*"))
                   if path.is_file() and path.name != "verification.json"
                   and path.relative_to(PROJECT) != Path("README.md")
                   and "target" not in path.relative_to(PROJECT).parts}
        self.assertEqual(receipt["project_file_sha256"], current)

    def test_scoped_afl_feedback_is_stable_and_input_dependent(self):
        feedback = json.loads((OVERLAY / "verification.json").read_text())
        base = sha256((PROJECT / "verification.json").read_bytes()).hexdigest()
        self.assertTrue(feedback["pass"])
        self.assertEqual(feedback["base_project_receipt_sha256"], base)
        self.assertEqual(feedback["control_sha256"], MANIFEST["control_sha256"])
        self.assertEqual(feedback["variant_sha256"], MANIFEST["afl_variant_sha256"])
        self.assertEqual(MANIFEST["afl_instrumented_crates"], [OWN_CRATE])
        self.assertEqual(set(feedback["sancov_scope"]["rlib_guard_bytes"]), {OWN_CRATE})
        self.assertGreaterEqual(feedback["repeats"], 10)
        self.assertTrue(feedback["control_stability"]["all_repeats_identical"])
        self.assertTrue(feedback["variant_stability"]["all_repeats_identical"])
        self.assertEqual(feedback["control_stability"]["stable_edges"], feedback["feedback_edges"])
        self.assertGreaterEqual(feedback["edges_only_in_control"] + feedback["edges_only_in_variant"], 2)
        self.assertEqual(feedback["control_output"], MANIFEST["expected_output"])
        self.assertEqual(feedback["variant_output"], MANIFEST["afl_variant_expected_output"])
        self.assertTrue(feedback["source_differential"]["files_with_different_line_counts"])
        self.assertTrue(feedback["fixed_hashmap_keys"]["replay_output_unchanged"])
        for name in ("Cargo.toml", "Cargo.lock", "afl_fuzzer.rs", "Dockerfile", "rustc-scope.sh",
                     "sancov_scope.py", "fixed_getrandom.c", "build.py"):
            self.assertEqual(feedback["overlay_file_sha256"][name],
                             sha256((OVERLAY / name).read_bytes()).hexdigest())

    def test_selected_and_ranked(self):
        cell_dir = ROOT / "data/rust/toml"
        cell = json.loads((cell_dir / "cell.json").read_text())
        parsers = json.loads((cell_dir / "parsers.json").read_text())
        leads = json.loads((cell_dir / "leads.json").read_text())
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(cell["unresolved_documentation_leads"], len(leads["leads"]))
        self.assertIn(f"projects/toml/rust/{SLUG}/verification.json", cell["third_party_control_results"])
        entry, = [parser for parser in parsers if parser["name"] == PACKAGE]
        self.assertEqual(entry["version"], MANIFEST["release"])
        self.assertEqual(entry["expected_output"], MANIFEST["expected_output"])
        self.assertNotIn("toml_parser (", entry["family"])
        snapshot = json.loads((cell_dir / "registry-snapshot.json").read_text())
        hit = next(hit for query in snapshot["search"] for hit in query["hits"] if hit["name"] == PACKAGE)
        self.assertEqual(entry["metric"]["value"], hit["recent_downloads"])
        self.assertNotIn(PACKAGE, {lead["name"] for lead in leads["leads"]})
        ranking = (cell_dir / "ranking.md").read_text()
        rows = [line for line in ranking.splitlines() if line.startswith("| ") and line[2].isdigit()]
        ranked = [int(row.split("|")[4].strip().replace(",", "")) for row in rows]
        self.assertEqual(ranked, sorted((parser["metric"]["value"] for parser in parsers), reverse=True))
        self.assertTrue(any(f"[{PACKAGE}]" in row for row in rows))


if __name__ == "__main__":
    unittest.main()
