"""Rust nanomp3: minimp3-port decode on both controls, shared family record and scoped AFL++ feedback."""

from hashlib import sha256
import json
import os
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
SLUG, PACKAGE = "nanomp3", "nanomp3"
PROJECT = ROOT / "projects/mp3/rust" / SLUG
OVERLAY = ROOT / "fuzzing/afl-native/mp3/rust" / SLUG
CELL = ROOT / "data/rust/mp3"
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "controls/mp3"))
from build_afl_rust import SCOPE_CHECK, SCOPE_WRAPPER, dockerfile  # noqa: E402
from check_controls import walk  # noqa: E402


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def oracle(control: str) -> dict:
    header = walk((ROOT / control).read_bytes())
    samples = header["frames"] * header["samples_per_frame"]
    return {"sample_rate": header["sample_rate"], "channels": header["channels"], "layer": 3,
            "bitrate_kbps": header["bitrate"] // 1000, "frames": header["frames"],
            "frame_bytes": header["frame_bytes"], "frame_samples_per_channel": samples,
            "samples_per_channel": samples, "pcm_samples": samples * header["channels"]}


class RustMp3Nanomp3PilotTest(unittest.TestCase):
    def test_controls_match_independent_header_walk(self):
        manifest = read(PROJECT / "manifest.json")
        parser, = [item for item in read(CELL / "parsers.json") if item["name"] == PACKAGE]
        for key, control in (("expected_output", manifest["control"]),
                             ("afl_variant_expected_output", manifest["afl_variant"])):
            expected = oracle(control)
            self.assertEqual({field: manifest[key][field] for field in expected}, expected, key)
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        self.assertEqual(parser["differential_expected_output"], manifest["afl_variant_expected_output"])
        self.assertEqual(read(PROJECT / "verification.json")["output"], manifest["expected_output"])

    def test_overlay_files_are_generated(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(OVERLAY / "verification.json")
        self.assertEqual((OVERLAY / "rustc-scope.sh").read_text(), SCOPE_WRAPPER)
        self.assertTrue(os.access(OVERLAY / "rustc-scope.sh", os.X_OK))
        self.assertEqual((OVERLAY / "sancov_scope.py").read_text(), SCOPE_CHECK)
        self.assertEqual((OVERLAY / "Dockerfile").read_text(),
                         dockerfile(Path(f"mp3/rust/{SLUG}"), manifest, receipt["afl_package"]))
        for name, digest in receipt["overlay_file_sha256"].items():
            self.assertEqual(sha256((OVERLAY / name).read_bytes()).hexdigest(), digest, name)
        self.assertEqual(receipt["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())

    def test_feedback_is_scoped_exact_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(OVERLAY / "verification.json")
        scoped = sorted(manifest["afl_instrumented_crates"])
        self.assertEqual(receipt["sancov_scope"]["instrumented_crates"], scoped)
        self.assertEqual(sorted(receipt["sancov_scope"]["rlib_guard_bytes"]), scoped)
        self.assertIn("serde_json", receipt["sancov_scope"]["uninstrumented_rlibs"])
        self.assertEqual([line for line in receipt["rustc_wrapper_log"] if line.startswith("instrumented ")],
                         [f"instrumented {crate}" for crate in scoped])
        for name, key in (("control", "expected_output"), ("variant", "afl_variant_expected_output")):
            walked = receipt["header_walk_oracle"][name]
            self.assertEqual(walked, {field: manifest[key][field] for field in walked})
        self.assertGreaterEqual(receipt["repeats"], 5)
        for key, digest, edges in (("control_stability", receipt["control_map_sha256"], receipt["feedback_edges"]),
                                   ("variant_stability", receipt["variant_map_sha256"],
                                    receipt["variant_feedback_edges"])):
            record = receipt[key]
            self.assertTrue(record["all_repeats_identical"])
            self.assertEqual(record["repeat_map_sha256"], [digest] * receipt["repeats"])
            self.assertEqual(record["repeat_tuple_counts"], [edges] * receipt["repeats"])
        self.assertNotEqual(receipt["control_map_sha256"], receipt["variant_map_sha256"])
        self.assertGreater(receipt["edges_only_in_control"], 0)
        self.assertGreater(receipt["edges_only_in_variant"], 0)
        own = receipt["own_source_differential"]
        self.assertTrue(own["lines_only_in_control"] and own["lines_only_in_variant"])
        self.assertIs(receipt["mutation_campaign_run"], False)

    def test_lead_is_selected_in_metric_order(self):
        parsers = read(CELL / "parsers.json")
        values = [item["metric"]["value"] for item in parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        lead, = [item for item in read(CELL / "leads.json")["unresolved_leads"] if item["name"] == PACKAGE]
        parser, = [item for item in parsers if item["name"] == PACKAGE]
        self.assertEqual(lead["status"], "selected")
        self.assertEqual(parser["metric"]["value"], lead["recent_downloads_90d"])
        hits = {hit["recent_downloads"] for search in read(CELL / "registry-snapshot.json")["search"]
                for hit in search["hits"] if hit["name"] == PACKAGE}
        self.assertEqual(hits, {parser["metric"]["value"]})

    def test_shared_minimp3_family_is_recorded(self):
        manifest = read(PROJECT / "manifest.json")
        parser, = [item for item in read(CELL / "parsers.json") if item["name"] == PACKAGE]
        minimp3, = [item for item in read(CELL / "parsers.json") if item["name"] == "minimp3"]
        self.assertIn("minimp3", parser["family"])
        self.assertIn(manifest["expected_output"]["minimp3_compat_pcm_sha256"][:8], parser["family_note"])
        self.assertIn(manifest["afl_variant_expected_output"]["minimp3_compat_pcm_sha256"][:8], parser["family_note"])
        # The compat PCM matches scalar minimp3.h, not the NEON build behind the minimp3 receipt.
        self.assertNotEqual(manifest["expected_output"]["minimp3_compat_pcm_sha256"],
                            minimp3["expected_output"]["pcm_sha256"])
        core, = [item for item in read(CELL / "leads.json")["unresolved_leads"] if item["name"] == "nanomp3-core"]
        self.assertEqual(core["status"], "excluded_shared_family")
        self.assertNotIn("nanomp3-core", {item["name"] for item in read(CELL / "parsers.json")})
        receipt = read(OVERLAY / "verification.json")
        self.assertTrue(receipt["underlying_source_differential"]["lines_only_in_variant"])
        self.assertGreater(read(PROJECT / "verification.json")["underlying_source_lines_covered"], 0)

    def test_smoke_rows_match_receipt(self):
        receipt = read(OVERLAY / "verification.json")
        row, = [item for item in read(ROOT / "data/afl-rust-smoke.json")["results"]
                if item["project"] == f"mp3/rust/{SLUG}"]
        self.assertEqual((row["feedback_edges"], row["image_id"]), (receipt["feedback_edges"], receipt["image_id"]))
        plan, = [item for item in read(ROOT / "data/afl-plan-smoke.json")["results"]
                 if item["project"] == f"mp3/rust/{SLUG}"]
        self.assertEqual(plan["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
