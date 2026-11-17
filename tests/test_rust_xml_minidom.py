"""Check the minidom controls, shared rxml family and scoped AFL++ evidence."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/xml/rust/minidom"
MANIFEST = json.loads((PROJECT / "manifest.json").read_text())
RXML = json.loads((ROOT / "projects/xml/rust/rxml/manifest.json").read_text())
spec = importlib.util.spec_from_file_location("xml_control_oracle", ROOT / "controls/xml/check_controls.py")
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)


class MinidomEvidenceTest(unittest.TestCase):
    def test_controls_match_independent_expat(self):
        for path_key, digest_key, output_key in (
            ("control", "control_sha256", "expected_output"),
            ("afl_variant", "afl_variant_sha256", "afl_variant_expected_output"),
        ):
            data = (ROOT / MANIFEST[path_key]).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), MANIFEST[digest_key])
            self.assertEqual(oracle.summarize(data), MANIFEST[output_key])
        # Same restricted second control as the selected rxml path.
        self.assertEqual(MANIFEST["afl_variant"], RXML["afl_variant"])
        self.assertEqual(MANIFEST["shared_second_control"], "controls/xml/order-default-ns.xml")

    def test_source_pins_and_shared_family_feedback(self):
        lock = tomllib.loads((PROJECT / "Cargo.lock").read_text())
        pins = {(package["name"], package["version"]): package.get("checksum") for package in lock["package"]}
        self.assertEqual(pins[("minidom", "0.19.0")], MANIFEST["source_sha256"])
        self.assertEqual(pins[("rxml", "0.14.0")], RXML["source_sha256"])
        self.assertEqual(MANIFEST["underlying_source_sha256"], RXML["source_sha256"])
        receipt = json.loads((PROJECT / "verification.json").read_text())
        self.assertGreater(receipt["parser_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        feedback = json.loads((ROOT / "fuzzing/afl-native/xml/rust/minidom/verification.json").read_text())
        self.assertEqual(set(feedback["sancov_scope"]["rlib_guard_bytes"]), {"minidom", "rxml", "rxml_validation"})
        self.assertGreaterEqual(feedback["repeats"], 10)
        self.assertTrue(feedback["control_stability"]["all_repeats_identical"])
        self.assertTrue(feedback["variant_stability"]["all_repeats_identical"])
        self.assertGreater(feedback["edges_only_in_control"], 0)
        self.assertGreater(feedback["edges_only_in_variant"], 0)
        self.assertEqual(feedback["shared_second_control_result"], 'XmlError(RestrictedXml("comments"))')
        self.assertIn("src/parser/raw.rs", feedback["source_differential"]["underlying_files_with_different_line_counts"])

    def test_selected_as_shared_family_and_ranked(self):
        cell_dir = ROOT / "data/rust/xml"
        cell = json.loads((cell_dir / "cell.json").read_text())
        parsers = json.loads((cell_dir / "parsers.json").read_text())
        leads = json.loads((cell_dir / "leads.json").read_text())
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(cell["unresolved_documentation_leads"], len(leads["unresolved_leads"]))
        self.assertIn("projects/xml/rust/minidom/verification.json", cell["third_party_control_results"])
        entry, = [parser for parser in parsers if parser["name"] == "minidom"]
        self.assertNotIn("candidate_for_selection", entry)
        self.assertIn("rxml", entry["family"])
        self.assertEqual(entry["metric"]["value"], 984597)
        self.assertNotIn("minidom", {lead["name"] for lead in leads["unresolved_leads"]})
        self.assertIn("minidom", {lead["name"] for lead in leads["verified_leads"]})
        ranking = (cell_dir / "ranking.md").read_text()
        self.assertIn("| 7 | [minidom]", ranking)
        rows = [line for line in ranking.splitlines() if line.startswith("| ") and line[2].isdigit()]
        ranked = [int(row.split("|")[4].strip().replace(",", "")) for row in rows]
        self.assertEqual(ranked, sorted((parser["metric"]["value"] for parser in parsers), reverse=True))


if __name__ == "__main__":
    unittest.main()
