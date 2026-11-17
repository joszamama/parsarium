"""The Java plain MP3 pilot keeps its selection, leads, and runtime inventory consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/java/mp3"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class JavaMp3PilotTest(unittest.TestCase):
    def test_selected_parser_is_highest_java_lead_and_kept_out_of_leads(self):
        parser, = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")
        metric = parser["popularity"]["value"]
        coordinate = f"{parser['group']}:{parser['artifact']}"
        self.assertNotIn(coordinate, {lead["coordinate"] for lead in leads})
        self.assertTrue(all(lead["status"].startswith(("unresolved", "excluded")) for lead in leads))
        # Only native wrappers may outrank the selection; they have no Java parser source.
        self.assertTrue(all(metric > lead["summed_direct_dependent_count"] for lead in leads
                            if lead["status"] != "excluded_native_wrapper"))
        snapshot = read(BASE / "registry-snapshot.json")
        recorded = snapshot["popularity_metric"]["packages"][coordinate]
        self.assertEqual(recorded["summed_direct_dependent_count"], metric)
        cell = read(BASE / "cell.json")
        self.assertEqual(sum(1 for lead in leads if lead["status"].startswith("unresolved")),
                         cell["unresolved_documentation_leads"])

    def test_same_family_as_id3v2_cell_is_recorded(self):
        parser, = read(BASE / "parsers.json")
        tagged, = [item for item in read(ROOT / "data/java/mp3_id3v2/parsers.json")
                   if item["name"] == parser["name"]]
        self.assertEqual(parser["family"], tagged["family"])

    def test_control_receipts_match_catalog(self):
        parser, = read(BASE / "parsers.json")
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
        result, = report["results"]
        manifest = read(ROOT / "projects/mp3/java/jcodec/manifest.json")
        overlay = ROOT / "fuzzing/afl-native/mp3/java/jcodec/verification.json"
        self.assertEqual(sha256(overlay.read_bytes()).hexdigest(), result["overlay_receipt_sha256"])
        self.assertTrue(result["pass"] and result["repeated_control_identical"])
        self.assertGreater(result["parser_feature_difference"], 0)
        self.assertGreater(result["afl_tuple_difference"], 0)
        self.assertEqual(result["differential_output"], manifest["differential_expected_output"])

    def test_no_standard_api_is_declared_not_omitted(self):
        standard = read(BASE / "standard.json")
        cell = read(BASE / "cell.json")
        self.assertEqual(standard["verified_apis"], [])
        self.assertEqual(cell["verified_standard_or_runtime_count"], 0)
        self.assertTrue(standard["no_api_findings"])


if __name__ == "__main__":
    unittest.main()
