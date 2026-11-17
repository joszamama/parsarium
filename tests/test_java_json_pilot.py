"""The Java JSON pilot keeps its selection, leads, and runtime inventory consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/java/json"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class JavaJsonPilotTest(unittest.TestCase):
    def test_selected_parser_is_highest_lead_and_kept_out_of_leads(self):
        parser, = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")
        metric = parser["popularity"]["value"]
        self.assertNotIn(parser["name"], {lead["name"] for lead in leads})
        self.assertTrue(all(lead["status"] == "unresolved" for lead in leads))
        self.assertTrue(all(metric > lead["summed_direct_dependent_count"] for lead in leads))
        snapshot = read(BASE / "registry-snapshot.json")
        recorded = snapshot["popularity_metric"]["packages"][
            f"{parser['group']}:{parser['artifact']}"]
        self.assertEqual(recorded["summed_direct_dependent_count"], metric)
        self.assertEqual(len(leads), read(BASE / "cell.json")["unresolved_documentation_leads"])

    def test_control_receipts_match_catalog(self):
        parser, = read(BASE / "parsers.json")
        project = ROOT / parser["project"]
        manifest = read(project / "manifest.json")
        receipt = read(project / "verification.json")
        self.assertEqual(manifest["release"], parser["version"])
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], parser["expected_output"])
        self.assertEqual(sha256((ROOT / manifest["control"]).read_bytes()).hexdigest(),
                         manifest["control_sha256"])
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((project / name).read_bytes()).hexdigest(), digest, name)

    def test_feedback_is_stable_and_differential(self):
        report = read(BASE / "afl-feedback.json")
        result, = report["results"]
        overlay = ROOT / "fuzzing/afl-native/json/java/jackson_databind/verification.json"
        self.assertEqual(sha256(overlay.read_bytes()).hexdigest(), result["overlay_receipt_sha256"])
        self.assertTrue(result["pass"] and result["repeated_control_identical"])
        self.assertGreater(result["parser_feature_difference"], 0)
        self.assertGreater(result["afl_tuple_difference"], 0)
        self.assertEqual(result["differential_output"]["root"], "array")

    def test_no_standard_api_is_declared_not_omitted(self):
        standard = read(BASE / "standard.json")
        cell = read(BASE / "cell.json")
        self.assertEqual(standard["verified_apis"], [])
        self.assertEqual(cell["verified_standard_or_runtime_count"], 0)
        self.assertTrue(standard["no_api_findings"])
        pilot = read(ROOT / "data/pilot-cells.json")["cells"]
        entry, = [item for item in pilot if (item["ecosystem"], item["format"]) == ("java", "json")]
        self.assertEqual(entry, {**cell, "phase": "pilot", "complete": False})


if __name__ == "__main__":
    unittest.main()
