"""Pin mp3-duration's frame-derived result and opt-in AFL++ hit-count bridge."""

from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "controls/mp3"))
sys.path.insert(0, str(ROOT / "scripts"))
from check_controls import walk  # noqa: E402
from build_afl_bridge import dockerfile  # noqa: E402


def read(path):
    return json.loads(path.read_text(encoding="utf-8"))


class Mp3DurationPathTest(unittest.TestCase):
    def setUp(self):
        self.project = ROOT / "projects/mp3/javascript/mp3_duration"
        self.manifest = read(self.project / "manifest.json")
        self.receipt = read(self.project / "verification.json")
        self.parser, = (item for item in read(ROOT / "data/javascript/mp3/parsers.json")
                        if item["name"] == "mp3-duration")
        self.result, = read(ROOT / "data/javascript/mp3/mp3_duration-feedback-differential.json")["results"]

    def test_both_durations_match_independent_frame_walker(self):
        for control_key, hash_key, output_key, frames in (
            ("control", "control_sha256", "expected_output", 11),
            ("differential_control", "differential_control_sha256", "differential_expected_output", 12),
        ):
            data = (ROOT / self.manifest[control_key]).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), self.manifest[hash_key])
            self.assertNotEqual(data[:3], b"ID3")
            info = walk(data)
            self.assertEqual(info["frames"], frames)
            expected = round(1000 * frames * info["samples_per_frame"] / info["sample_rate"])
            self.assertEqual(self.manifest[output_key], {"duration_ms": expected})
        self.assertEqual(self.receipt["output"], self.manifest["expected_output"])
        self.assertEqual(self.result["differential_output"], self.manifest["differential_expected_output"])

    def test_release_adoption_and_shared_package_are_pinned(self):
        source = read(self.project / "source-lock.json")["mp3-duration"]
        tagged = read(ROOT / "projects/mp3_id3v2/javascript/mp3_duration/source-lock.json")["mp3-duration"]
        packages = read(self.project / "package-lock.json")["packages"]
        self.assertEqual(source["source_sha256"], tagged["source_sha256"])
        self.assertEqual(source["npm_integrity"], tagged["npm_integrity"])
        self.assertEqual(source["npm_integrity"], packages["node_modules/mp3-duration"]["integrity"])
        for name, item in source["dependencies"].items():
            self.assertEqual(packages[f"node_modules/{name}"]["version"], item["release"])
            self.assertEqual(packages[f"node_modules/{name}"]["integrity"], item["npm_integrity"])
        lead, = (item for item in read(ROOT / "data/javascript/mp3/leads.json")
                 if item["name"] == "mp3-duration")
        snapshot = read(ROOT / "data/javascript/mp3/registry-snapshot.json")
        self.assertEqual(lead["status"], "promoted_to_verified")
        self.assertEqual(self.parser["metric"]["value"], snapshot["downloads"]["mp3-duration"]["downloads"])

    def test_parser_source_and_repeatable_frame_count_feedback(self):
        self.assertTrue(self.receipt["pass"])
        self.assertEqual(self.receipt["parser_source_files"], 1)
        self.assertGreater(self.receipt["parser_source_lines_covered"], 0)
        overlay_path = ROOT / "fuzzing/afl-native/mp3/javascript/mp3_duration/verification.json"
        overlay = read(overlay_path)
        self.assertEqual(overlay["base_image_id"], self.receipt["image_id"])
        self.assertEqual(self.result["overlay_receipt_sha256"], sha256(overlay_path.read_bytes()).hexdigest())
        self.assertEqual(self.result["no_parse_parser_features"], 0)
        self.assertEqual(self.result["repeats_per_control"], 3)
        self.assertTrue(self.result["repeated_control_identical"])
        self.assertTrue(self.result["repeated_differential_identical"])
        self.assertEqual(self.result["control_parser_calls"],
                         {"parseFrameHeader": [11], "frameSize": [11]})
        self.assertEqual(self.result["differential_parser_calls"],
                         {"parseFrameHeader": [12], "frameSize": [12]})
        self.assertGreater(self.result["parser_feature_difference"], 0)
        self.assertGreater(self.result["afl_tuple_difference"], 0)
        self.assertTrue(all(item.startswith("/work/node_modules/mp3-duration/index.js:")
                            for item in self.result["control_only_features"] + self.result["differential_only_features"]))
        self.assertTrue(all(item.endswith(":hits=11") for item in self.result["control_only_features"]))
        self.assertTrue(all(item.endswith(":hits=12") for item in self.result["differential_only_features"]))

    def test_opt_in_bridge_leaves_default_javascript_overlay_unchanged(self):
        existing = read(ROOT / "projects/mp3/javascript/codec_parser/manifest.json")
        relative = Path("mp3/javascript/codec_parser")
        default = dockerfile("parsarium/mp3-javascript-codec_parser:local", existing["platform"],
                             relative, existing["coverage_subject_prefix"], "javascript",
                             None, existing["fuzz_entry"], {}, "4.21c-5")
        self.assertEqual(default, (ROOT / "fuzzing/afl-native/mp3/javascript/codec_parser/Dockerfile").read_text())
        count = dockerfile("parsarium/mp3-javascript-mp3_duration:local", self.manifest["platform"],
                           Path("mp3/javascript/mp3_duration"), self.manifest["afl_coverage_subject_prefix"],
                           "javascript", None, self.manifest["fuzz_entry"], {}, "4.21c-5",
                           javascript_trace_name="javascript_count_trace.js",
                           javascript_count_functions=tuple(self.manifest["afl_js_count_functions"]))
        self.assertEqual(count, (ROOT / "fuzzing/afl-native/mp3/javascript/mp3_duration/Dockerfile").read_text())


if __name__ == "__main__":
    unittest.main()
