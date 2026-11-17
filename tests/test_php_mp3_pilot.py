"""The PHP plain MP3 pilot keeps its selection, oracle checks, and feedback receipts consistent."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/mp3"
FEEDBACK = {"getid3": BASE / "afl-feedback.json",
            "wapmorgan_mp3info": BASE / "wapmorgan_mp3info-feedback.json"}


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PhpMp3PilotTest(unittest.TestCase):
    def test_selected_parsers_are_ranked_by_recorded_downloads(self):
        parsers = read(BASE / "parsers.json")
        self.assertEqual([parser["name"] for parser in parsers], ["james-heinrich/getid3", "wapmorgan/mp3info"])
        values = [parser["metric"]["value"] for parser in parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        downloads = {hit["name"]: hit["downloads"] for query in read(BASE / "registry-snapshot.json")["search"]
                     for hit in query["hits"]}
        for parser in parsers:
            self.assertEqual(downloads[parser["name"]], parser["metric"]["value"])

    def test_leads_and_cell_counts_agree(self):
        leads = read(BASE / "leads.json")["leads"]
        cell = read(BASE / "cell.json")
        selected = {lead["name"] for lead in leads if lead["status"] == "selected"}
        self.assertEqual(selected, {parser["name"] for parser in read(BASE / "parsers.json")})
        self.assertEqual(cell["verified_third_party_count"], len(selected))
        self.assertEqual(dict(Counter(lead["status"] for lead in leads)), cell["leads_by_status"])
        self.assertEqual(cell["leads_recorded"], len(leads))

    def test_mp3info_is_independent_of_getid3(self):
        getid3, mp3info = read(BASE / "parsers.json")
        self.assertNotEqual(getid3["family"], mp3info["family"])
        lock = read(ROOT / "projects/mp3/php/wapmorgan_mp3info/composer.lock")
        self.assertNotIn("james-heinrich/getid3", {package["name"] for package in lock["packages"]})

    def test_control_receipts_match_catalog(self):
        for parser in read(BASE / "parsers.json"):
            slug = "getid3" if parser["name"] == "james-heinrich/getid3" else "wapmorgan_mp3info"
            project = ROOT / "projects/mp3/php" / slug
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
            lock = read(project / "source-lock.json")[parser["name"]]
            self.assertEqual(lock["source_sha256"], manifest["source_sha256"])
            self.assertIn(lock["source_sha256"], (project / "Dockerfile").read_text())

    def test_mp3info_oracle_comparison_is_recorded_exactly(self):
        sys.path.insert(0, str(ROOT / "controls/mp3"))
        from check_controls import walk
        mp3info = read(BASE / "parsers.json")[1]
        report = read(FEEDBACK["wapmorgan_mp3info"])
        first, second = report["oracle_comparison"]
        for result in (first, second):
            walked = walk((ROOT / result["control"]).read_bytes())
            self.assertEqual(result["oracle"]["frames"], walked["frames"])
            self.assertEqual(result["oracle"]["sample_rate"], walked["sample_rate"])
            self.assertEqual(result["oracle"]["bitrate"], walked["bitrate"])
        # The primary MPEG-1 control matches the header walk; the MPEG-2
        # control is misread and must stay recorded as a mismatch.
        self.assertTrue(first["header_fields_match"] and first["frames_match"] and first["audio_bytes_match"])
        self.assertEqual(first["observed"], mp3info["expected_output"])
        self.assertFalse(second["header_fields_match"] or second["frames_match"])
        self.assertEqual(second["observed"], mp3info["differential_expected_output"])
        for key in ("header_fields_match", "frames_match", "audio_bytes_match"):
            self.assertEqual(mp3info["oracle_comparison"][first["control"]][key], first[key])
            self.assertEqual(mp3info["oracle_comparison"][second["control"]][key], second[key])

    def test_feedback_is_parser_derived_stable_and_differential(self):
        for slug, path in FEEDBACK.items():
            result = read(path)
            manifest = read(ROOT / f"projects/mp3/php/{slug}/manifest.json")
            project_receipt = ROOT / f"projects/mp3/php/{slug}/verification.json"
            overlay = ROOT / f"fuzzing/afl-native/mp3/php/{slug}/verification.json"
            self.assertEqual(sha256(project_receipt.read_bytes()).hexdigest(), result["base_project_receipt_sha256"])
            self.assertEqual(sha256(overlay.read_bytes()).hexdigest(), result["overlay_receipt_sha256"])
            self.assertTrue(result["pass"] and result["repeated_controls_identical"])
            self.assertGreater(result["parser_feature_difference"], 0)
            self.assertGreater(result["afl_tuple_difference"], 0)
            self.assertEqual(result["second_control_output"], manifest["differential_expected_output"])
            self.assertIn(manifest["coverage_subject_prefix"], result["feedback_scope"])
        lines = read(FEEDBACK["wapmorgan_mp3info"])["differing_parser_lines"]
        self.assertTrue(lines and all(line.startswith("/work/vendor/wapmorgan/mp3info/src/") for line in lines))

    def test_no_standard_api_is_declared_not_omitted(self):
        standard = read(BASE / "standard.json")
        self.assertEqual(standard["verified_apis"], [])
        self.assertEqual(read(BASE / "cell.json")["verified_standard_or_runtime_count"], 0)
        self.assertTrue(standard["no_api_findings"])


if __name__ == "__main__":
    unittest.main()
