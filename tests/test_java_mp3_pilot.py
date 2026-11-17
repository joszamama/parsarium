"""The Java plain MP3 pilot keeps its selection, leads, and runtime inventory consistent."""

from hashlib import sha256
import json
from pathlib import Path
import runpy
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/java/mp3"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class JavaMp3PilotTest(unittest.TestCase):
    def test_selected_parsers_have_recorded_metrics_and_stay_out_of_leads(self):
        parsers = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")
        self.assertEqual([parser["name"] for parser in parsers],
                         ["jcodec", "mp3spi", "jlayer", "jaudiotagger", "mp3agic"])
        self.assertTrue(all(lead["status"].startswith(("unresolved", "excluded")) for lead in leads))
        # The highest selected pure-Java path outranks remaining unresolved leads.
        self.assertTrue(all(parsers[0]["popularity"]["value"] > lead["summed_direct_dependent_count"] for lead in leads
                            if lead["status"] != "excluded_native_wrapper"))
        snapshot = read(BASE / "registry-snapshot.json")
        for parser in parsers:
            coordinate = f"{parser['group']}:{parser['artifact']}"
            self.assertNotIn(coordinate, {lead["coordinate"] for lead in leads})
            recorded = snapshot["popularity_metric"]["packages"][coordinate]
            self.assertEqual(recorded["summed_direct_dependent_count"],
                             parser["popularity"]["value"])
        cell = read(BASE / "cell.json")
        self.assertEqual(sum(1 for lead in leads if lead["status"].startswith("unresolved")),
                         cell["unresolved_documentation_leads"])

    def test_same_family_as_id3v2_cell_is_recorded(self):
        parser = next(item for item in read(BASE / "parsers.json") if item["name"] == "jcodec")
        tagged, = [item for item in read(ROOT / "data/java/mp3_id3v2/parsers.json")
                   if item["name"] == parser["name"]]
        self.assertEqual(parser["family"], tagged["family"])
        jlayer = next(item for item in read(BASE / "parsers.json") if item["name"] == "jlayer")
        self.assertNotEqual(parser["family"], jlayer["family"])
        mp3spi = next(item for item in read(BASE / "parsers.json") if item["name"] == "mp3spi")
        self.assertIn("same JLayer decoder lineage", mp3spi["family_note"])
        self.assertEqual(mp3spi["underlying_family"], jlayer["underlying_family"])
        self.assertGreater(read(ROOT / mp3spi["project"] / "verification.json")["underlying_source_lines_covered"], 0)
        header = next(item for item in read(BASE / "parsers.json") if item["name"] == "jaudiotagger")
        self.assertEqual(header["family"], next(item for item in read(
            ROOT / "data/java/mp3_id3v2/parsers.json") if item["name"] == "jaudiotagger")["family"])
        self.assertNotIn("frames", header["expected_output"])
        self.assertNotIn("decoded_samples", header["expected_output"])
        self.assertIn("byte 104", read(ROOT / header["project"] / "manifest.json")["coverage_limit"])
        mp3agic = next(item for item in read(BASE / "parsers.json")
                        if item["name"] == "mp3agic")
        self.assertEqual(mp3agic["family"], next(item for item in read(
            ROOT / "data/java/mp3_id3v2/parsers.json") if item["name"] == "mp3agic")["family"])
        self.assertNotIn("frames", mp3agic["expected_output"])
        self.assertNotIn("duration", mp3agic["expected_output"])
        self.assertIn("261 ms", read(ROOT / mp3agic["project"] / "manifest.json")["coverage_limit"])

    def test_control_receipts_match_catalog(self):
        for parser in read(BASE / "parsers.json"):
            project = ROOT / parser["project"]
            manifest = read(project / "manifest.json")
            receipt = read(project / "verification.json")
            self.assertEqual(manifest["release"], parser["version"])
            self.assertTrue(receipt["pass"])
            self.assertEqual(receipt["output"], parser["expected_output"])
            self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
            for key in ("control", "differential_control"):
                self.assertEqual(sha256((ROOT / manifest[key]).read_bytes()).hexdigest(),
                                 manifest[f"{key}_sha256"])
            for name, digest in receipt["project_file_sha256"].items():
                self.assertEqual(sha256((project / name).read_bytes()).hexdigest(), digest, name)

    def test_feedback_is_stable_and_differential(self):
        report = read(BASE / "afl-feedback.json")
        # The cell aggregate is refreshed by the integrator. The new path's
        # scoped receipt is testable before that aggregate is regenerated.
        scoped = [read(ROOT / f"data/java/mp3/{slug}-feedback-differential.json")
                  for slug in ("jlayer", "mp3spi", "jaudiotagger", "mp3agic")]
        results = {item["project"]: item for item in [*report["results"], *scoped]}
        self.assertEqual(set(results), {"mp3/java/jcodec", "mp3/java/jlayer",
                                        "mp3/java/mp3spi", "mp3/java/jaudiotagger",
                                        "mp3/java/mp3agic"})
        for result in results.values():
            slug = result["project"].rsplit("/", 1)[-1]
            manifest = read(ROOT / f"projects/mp3/java/{slug}/manifest.json")
            overlay = ROOT / f"fuzzing/afl-native/mp3/java/{slug}/verification.json"
            self.assertEqual(sha256(overlay.read_bytes()).hexdigest(), result["overlay_receipt_sha256"])
            self.assertTrue(result["pass"] and result["repeated_control_identical"])
            self.assertGreater(result["parser_feature_difference"], 0)
            self.assertGreater(result["afl_tuple_difference"], 0)
            self.assertEqual(result["differential_output"], manifest["differential_expected_output"])
        mp3spi_groups = results["mp3/java/mp3spi"]["source_groups"]
        self.assertGreater(mp3spi_groups["wrapper"]["control_features"], 0)
        self.assertGreater(mp3spi_groups["core"]["feature_difference"], 0)

    def test_no_standard_api_is_declared_not_omitted(self):
        standard = read(BASE / "standard.json")
        cell = read(BASE / "cell.json")
        self.assertEqual(standard["verified_apis"], [])
        self.assertEqual(cell["verified_standard_or_runtime_count"], 0)
        self.assertTrue(standard["no_api_findings"])

    def test_jaudiotagger_header_fields_match_independent_frame_walker(self):
        parser = next(item for item in read(BASE / "parsers.json")
                      if item["name"] == "jaudiotagger")
        walk = runpy.run_path(str(ROOT / "controls/mp3/check_controls.py"))["walk"]
        for path_key, output_key in (("control", "expected_output"),
                                     ("differential_control", "differential_expected_output")):
            oracle = walk((ROOT / parser[path_key]).read_bytes())
            observed = parser[output_key]
            self.assertEqual(observed["sample_rate"], oracle["sample_rate"])
            self.assertEqual(observed["channels"], oracle["channels"])
            self.assertEqual(observed["bitrate_kbps"] * 1000, oracle["bitrate"])

    def test_mp3agic_claimed_fields_match_independent_frame_walker(self):
        parser = next(item for item in read(BASE / "parsers.json")
                      if item["name"] == "mp3agic")
        walk = runpy.run_path(str(ROOT / "controls/mp3/check_controls.py"))["walk"]
        for path_key, output_key in (("control", "expected_output"),
                                     ("differential_control", "differential_expected_output")):
            oracle = walk((ROOT / parser[path_key]).read_bytes())
            observed = parser[output_key]
            self.assertEqual(observed["sample_rate"], oracle["sample_rate"])
            self.assertEqual(1 if observed["channel_mode"] == "Mono" else 2,
                             oracle["channels"])
            self.assertEqual(observed["bitrate_kbps"] * 1000, oracle["bitrate"])


if __name__ == "__main__":
    unittest.main()
