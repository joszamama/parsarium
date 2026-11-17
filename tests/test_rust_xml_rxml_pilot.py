"""The Rust rxml XML path keeps its pins, restricted controls, family and feedback consistent."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/rust/xml"
PROJECT = ROOT / "projects/xml/rust/rxml"
OVERLAY = ROOT / "fuzzing/afl-native/xml/rust/rxml"
SOURCE = "4959705975475401c48b375deedd848d15b816c3915978fc617b31a1776fb60a"
VALIDATION = "4895cf728e9ef2b921d1b80793affb1a2d2e0cbd6c24555c18e25d8aee0124b8"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def oracle():
    spec = importlib.util.spec_from_file_location("check_controls", ROOT / "controls/xml/check_controls.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class RustXmlRxmlPilotTest(unittest.TestCase):
    def test_pins_agree(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual((manifest["release"], lock["rxml"]["release"]), ("0.14.0", "0.14.0"))
        self.assertEqual(manifest["source_sha256"], SOURCE)
        self.assertEqual(lock["rxml"]["source_sha256"], SOURCE)
        self.assertEqual(lock["rxml_validation"]["source_sha256"], VALIDATION)
        for digest in (SOURCE, VALIDATION, manifest["base_image"], manifest["runtime_base_image"]):
            self.assertIn(digest, dockerfile)
        for cargo_lock in (PROJECT / "Cargo.lock", OVERLAY / "Cargo.lock"):
            packages = {item["name"]: item for item in tomllib.loads(cargo_lock.read_text())["package"]}
            self.assertEqual(packages["rxml"]["checksum"], SOURCE)
            self.assertEqual(packages["rxml_validation"]["checksum"], VALIDATION)
            # No shared_ns interner, tokio or compact_str in the parsed path.
            self.assertNotIn("weak-table", packages)
            self.assertNotIn("tokio", packages)

    def test_controls_match_expat_oracle(self):
        manifest = read(PROJECT / "manifest.json")
        check = oracle()
        for path, digest, expected in (
                (manifest["control"], manifest["control_sha256"], manifest["expected_output"]),
                (manifest["afl_variant"], manifest["afl_variant_sha256"], manifest["afl_variant_expected_output"])):
            data = (ROOT / path).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), digest)
            self.assertEqual(check.CONTROLS[Path(path).name], digest)
            self.assertEqual(check.summarize(data), expected)
        shared = (ROOT / manifest["shared_second_control"]).read_bytes()
        self.assertEqual(sha256(shared).hexdigest(), manifest["shared_second_control_sha256"])
        self.assertEqual(check.summarize(shared), manifest["afl_variant_expected_output"])
        # The restricted control drops only the comment and processing instruction.
        removed = set(shared.decode().splitlines()) - set((ROOT / manifest["afl_variant"]).read_text().splitlines())
        self.assertEqual(removed, {"<!-- order receipt -->", '  <?audit step="1"?>'})

    def test_receipts_match_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "rxml"]
        self.assertTrue(receipt["pass"] and receipt["fuzz_engine_smoke_pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        self.assertEqual(parser["second_control_expected_output"], manifest["afl_variant_expected_output"])
        self.assertEqual(parser["shared_second_control_result"], 'Error(RestrictedXml("comments"))')
        self.assertIn("no processing instructions", parser["restricted_features"])
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertEqual(parser["metric"]["value"], 961809)

    def test_cell_records_selected_lead(self):
        parsers = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")
        cell = read(BASE / "cell.json")
        self.assertNotIn("rxml", {lead["name"] for lead in leads["unresolved_leads"]})
        self.assertIn("rxml", {lead["name"] for lead in leads["verified_leads"]})
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(cell["unresolved_documentation_leads"], len(leads["unresolved_leads"]))
        self.assertIn("projects/xml/rust/rxml/verification.json", cell["third_party_control_results"])
        self.assertIn("| 8 | [rxml]", (BASE / "ranking.md").read_text())

    def test_feedback_is_stable_and_parser_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        self.assertTrue(overlay["pass"])
        self.assertEqual(overlay["parser_source_sha256"], SOURCE)
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(overlay["base_image_id"], read(PROJECT / "verification.json")["image_id"])
        for name, digest in overlay["overlay_file_sha256"].items():
            self.assertEqual(sha256((OVERLAY / name).read_bytes()).hexdigest(), digest, name)
        for key in ("control_stability", "variant_stability"):
            self.assertTrue(overlay[key]["all_repeats_identical"])
            self.assertEqual(overlay[key]["stable_ratio"], 1.0)
        self.assertGreater(overlay["edges_only_in_control"], 0)
        self.assertGreater(overlay["edges_only_in_variant"], 0)
        self.assertEqual(overlay["variant_output"], manifest["afl_variant_expected_output"])
        self.assertNotEqual(overlay["shared_second_control_exit_code"], 0)
        differing = overlay["source_differential"]["files_with_different_line_counts"]
        self.assertIn("src/lexer/mod.rs", differing)
        self.assertIn("src/parser/raw.rs", differing)


if __name__ == "__main__":
    unittest.main()
