"""Keep the verified mpg123-decoder controls separate from selected feedback paths."""

from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "controls/mp3"))
from check_controls import walk  # noqa: E402


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


class Mpg123DecoderLeadTest(unittest.TestCase):
    def test_control_evidence_and_feedback_blocker(self):
        lead, = (item for item in read(ROOT / "data/javascript/mp3/plain-mp3-pilot/leads.json")
                 if item["name"] == "mpg123-decoder")
        report = read(ROOT / lead["control_evidence"])
        lock = read(ROOT / "projects/mp3_id3v2/javascript/audio_decode_mp3/package-lock.json")
        selected = {item["name"] for item in read(ROOT / "data/javascript/mp3/parsers.json")}
        snapshot = read(ROOT / "data/javascript/mp3/plain-mp3-pilot/registry-snapshot.json")
        self.assertEqual(lead["status"], "unresolved_shared_family")
        self.assertNotIn("mpg123-decoder", selected)
        self.assertEqual(lead["npm_downloads_30d"], snapshot["downloads"]["mpg123-decoder"]["downloads"])
        self.assertEqual(report["npm_integrity"], lock["packages"]["node_modules/mpg123-decoder"]["integrity"])
        fixture = ROOT / report["dependency_fixture"] / "package-lock.json"
        self.assertEqual(report["dependency_lock_sha256"], sha256(fixture.read_bytes()).hexdigest())
        self.assertEqual(report["selection"], "verified_control_feedback_blocked_unselected")
        self.assertIsNone(report["parser_source_line_coverage"])
        self.assertEqual(report["afl_parser_feedback"], "blocked")
        self.assertEqual(report["node_v8_profile_wasm_scripts"], [])
        self.assertEqual(report["wasm_module"]["bytes"], 99479)
        self.assertTrue(all(value == 0 for value in report["wasm_module"]["custom_sections"].values()))
        for case in report["controls"]:
            data = (ROOT / case["control"]).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), case["sha256"])
            oracle = walk(data)
            self.assertEqual(oracle, case["oracle"])
            output = case["verified_output"]
            self.assertEqual(output["sample_rate"], oracle["sample_rate"])
            self.assertEqual(output["samples_decoded"], oracle["frames"] * oracle["samples_per_frame"])
            self.assertEqual(output["errors"], [])
            self.assertEqual(output["wasm"], report["wasm_module"])
        self.assertEqual(report["controls"][0]["verified_output"]["channel_lengths"], [12672, 12672])
        self.assertEqual(report["controls"][0]["oracle"]["channels"], 1)


if __name__ == "__main__":
    unittest.main()
