"""The JavaScript plain MP3 pilot keeps its selection, leads, receipts, and walker agreement consistent."""

from collections import Counter
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/javascript/mp3"
_spec = importlib.util.spec_from_file_location("check_controls", ROOT / "controls/mp3/check_controls.py")
WALKER = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(WALKER)


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class JavaScriptMp3PilotTest(unittest.TestCase):
    def test_selected_parsers_are_ranked_and_leads_preserve_discovery(self):
        parsers = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")
        cell = read(BASE / "cell.json")
        downloads = read(BASE / "registry-snapshot.json")["downloads"]
        self.assertEqual([parser["name"] for parser in parsers],
                         ["mediabunny", "music-metadata", "codec-parser", "mp3-duration", "mp3-parser"])
        values = [parser["metric"]["value"] for parser in parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        for parser in parsers:
            self.assertEqual(downloads[parser["name"]]["downloads"], parser["metric"]["value"])
            self.assertEqual(downloads[parser["name"]]["latest_version"], parser["version"])
        self.assertEqual({parser["name"] for parser in parsers} & {lead["name"] for lead in leads},
                         {"mp3-duration", "mp3-parser"})
        self.assertTrue(all(lead["status"] == "promoted_to_verified" for lead in leads
                            if lead["name"] in {"mp3-duration", "mp3-parser"}))
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(cell["leads_recorded"], len(leads))
        self.assertEqual(cell["leads_by_status"], dict(Counter(lead["status"] for lead in leads)))
        self.assertEqual(cell["third_party_control_results"],
                         [f"{parser['project']}/verification.json" for parser in parsers])

    def test_parser_families_are_independent(self):
        parsers = read(BASE / "parsers.json")
        self.assertEqual(len({parser["family"] for parser in parsers}), len(parsers))
        codec_parser = next(parser for parser in parsers if parser["name"] == "codec-parser")
        self.assertEqual(codec_parser["dependencies"], [])
        lock = read(ROOT / codec_parser["project"] / "package-lock.json")["packages"]
        self.assertNotIn("dependencies", lock["node_modules/codec-parser"])

    def test_control_receipts_match_catalog(self):
        for parser in read(BASE / "parsers.json"):
            project = ROOT / parser["project"]
            manifest = read(project / "manifest.json")
            receipt = read(project / "verification.json")
            lock = read(project / "source-lock.json")[parser["name"]]
            self.assertEqual(manifest["release"], parser["version"])
            self.assertEqual(lock["source_sha256"], manifest["source_sha256"])
            self.assertEqual(lock["license"], parser["license"])
            self.assertTrue(receipt["pass"])
            self.assertEqual(receipt["output"], parser["expected_output"])
            self.assertGreater(receipt["parser_source_lines_covered"], 0)
            for key in ("control", "differential_control"):
                self.assertEqual(sha256((ROOT / manifest[key]).read_bytes()).hexdigest(),
                                 manifest[f"{key}_sha256"])
            for name, digest in receipt["project_file_sha256"].items():
                self.assertEqual(sha256((project / name).read_bytes()).hexdigest(), digest, name)

    def test_codec_parser_outputs_match_frame_header_walker(self):
        manifest = read(ROOT / "projects/mp3/javascript/codec_parser/manifest.json")
        for control, output in ((manifest["control"], manifest["expected_output"]),
                                (manifest["differential_control"], manifest["differential_expected_output"])):
            data = (ROOT / control).read_bytes()
            walked = WALKER.walk(data)
            self.assertEqual({key: output[key] for key in walked}, walked)
            self.assertEqual(output["frame_bytes"], len(data))
            self.assertEqual(output["total_samples"], walked["frames"] * walked["samples_per_frame"])
            self.assertEqual(output["header_variants"], 1)

    def test_mp3_parser_walks_both_valid_controls_with_documented_data_view_api(self):
        project = ROOT / "projects/mp3/javascript/mp3_parser"
        manifest = read(project / "manifest.json")
        adapter = (project / "adapter.mjs").read_text(encoding="utf-8")
        self.assertIn("mp3Parser.readFrame(view, offset, false)", adapter)
        self.assertIn("new DataView(bytes.buffer, bytes.byteOffset, bytes.byteLength)", adapter)
        self.assertEqual(manifest["coverage_subject_prefix"],
                         "/work/node_modules/mp3-parser/lib/lib.js")
        for control, output in ((manifest["control"], manifest["expected_output"]),
                                (manifest["differential_control"], manifest["differential_expected_output"])):
            data = (ROOT / control).read_bytes()
            walked = WALKER.walk(data)
            self.assertEqual({key: output[key] for key in walked}, walked)
            self.assertEqual(output["total_samples"], walked["frames"] * walked["samples_per_frame"])
            self.assertEqual(output["mpeg_version_bits"], format((data[1] >> 3) & 3, "02b"))
            self.assertEqual(output["layer"], "Layer III")
            self.assertEqual(output["header_variants"], 1)
        npm_lock = read(project / "package-lock.json")["packages"]["node_modules/mp3-parser"]
        source_lock = read(project / "source-lock.json")["mp3-parser"]
        self.assertEqual(npm_lock["integrity"], source_lock["npm_integrity"])
        self.assertNotIn("dependencies", npm_lock)

    def test_music_metadata_outputs_match_header_oracle(self):
        manifest = read(ROOT / "projects/mp3/javascript/music_metadata/manifest.json")
        for control, output in ((manifest["control"], manifest["expected_output"]),
                                (manifest["differential_control"], manifest["differential_expected_output"])):
            data = (ROOT / control).read_bytes()
            walked = WALKER.walk(data)
            samples = walked["frames"] * walked["samples_per_frame"]
            version = {3: 1, 2: 2, 0: 2.5}[(data[1] >> 3) & 3]
            layer = 4 - ((data[1] >> 1) & 3)
            self.assertEqual(output["codec"], f"MPEG {version} Layer {layer}")
            self.assertEqual((output["mpeg_version"], output["layer"]), (version, layer))
            for key in ("sample_rate", "channels", "bitrate"):
                self.assertEqual(output[key], walked[key], key)
            self.assertEqual(output["number_of_samples"], samples)
            self.assertEqual(output["duration"], samples / walked["sample_rate"])
            # Untagged controls: the result must come from MPEG frames, not tag metadata.
            self.assertEqual((output["tag_types"], output["warnings"]), ([], 0))

    def test_music_metadata_pins_runtime_dependencies(self):
        project = ROOT / "projects/mp3/javascript/music_metadata"
        lock = read(project / "source-lock.json")["music-metadata"]
        packages = read(project / "package-lock.json")["packages"]
        self.assertEqual(packages["node_modules/music-metadata"]["integrity"], lock["npm_integrity"])
        self.assertEqual(set(packages["node_modules/music-metadata"]["dependencies"]) - set(lock["runtime_dependencies"]), set())
        for name, pinned in lock["runtime_dependencies"].items():
            entry = packages[f"node_modules/{name}"]
            self.assertEqual((entry["version"], entry["integrity"], entry["license"]),
                             (pinned["version"], pinned["npm_integrity"], pinned["license"]), name)
            self.assertEqual(set(entry.get("dependencies", {})) - set(lock["runtime_dependencies"]), set(), name)

    def test_feedback_is_stable_and_differential(self):
        # The cell aggregate is refreshed by the integrator. The new path's
        # scoped receipt is testable before that aggregate is regenerated.
        report = read(BASE / "afl-feedback.json")
        scoped = [read(BASE / f"{slug}-feedback-differential.json")
                  for slug in ("codec_parser", "music_metadata", "mp3_parser")]
        results = {item["project"]: item for item in [*report["results"], *scoped]}
        self.assertEqual(set(results), {"mp3/javascript/mediabunny", "mp3/javascript/music_metadata",
                                        "mp3/javascript/codec_parser", "mp3/javascript/mp3_parser",
                                        "mp3/javascript/mp3_duration"})
        for result in results.values():
            slug = result["project"].rsplit("/", 1)[-1]
            manifest = read(ROOT / f"projects/mp3/javascript/{slug}/manifest.json")
            overlay = ROOT / f"fuzzing/afl-native/mp3/javascript/{slug}/verification.json"
            self.assertEqual(sha256(overlay.read_bytes()).hexdigest(), result["overlay_receipt_sha256"])
            self.assertTrue(result["pass"] and result["repeated_control_identical"]
                            and result["repeated_differential_identical"])
            self.assertGreater(result["parser_feature_difference"], 0)
            self.assertGreater(result["afl_tuple_difference"], 0)
            self.assertEqual(result["differential_output"], manifest["differential_expected_output"])
        self.assertIn("frame_bytes", scoped[0]["control_walker"]["compared_fields"])
        music = results["mp3/javascript/music_metadata"]
        self.assertGreaterEqual(music["repeats_per_control"], 3)
        self.assertEqual(music["control_only_features"], [])
        self.assertTrue(all(item.startswith("MpegParser.js:") for item in music["differential_only_features"]))
        for walker in (music["control_walker"], music["differential_walker"]):
            self.assertTrue({"mpeg_version", "layer", "number_of_samples", "duration"} <= set(walker["compared_fields"]))
        for apis in music["documented_api_agreement"].values():
            self.assertEqual(apis, ["parseBuffer", "parseFile", "parseStream"])
        frame = results["mp3/javascript/mp3_parser"]
        self.assertEqual(frame["control_only_features_by_file"], {"lib/lib.js": 2})
        self.assertEqual(frame["differential_only_features_by_file"], {"lib/lib.js": 0})
        self.assertEqual(frame["repeats_per_control"], 3)

    def test_no_standard_api_is_declared_not_omitted(self):
        standard = read(BASE / "standard.json")
        self.assertEqual(standard["verified_apis"], [])
        self.assertEqual(read(BASE / "cell.json")["verified_standard_or_runtime_count"], 0)
        self.assertTrue(standard["no_api_findings"])


if __name__ == "__main__":
    unittest.main()
