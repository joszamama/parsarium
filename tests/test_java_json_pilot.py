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
    def test_selected_parsers_are_ordered_and_kept_out_of_leads(self):
        parsers = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")
        metrics = [parser["popularity"]["value"] for parser in parsers]
        self.assertEqual([parser["name"] for parser in parsers],
                         ["jackson-databind", "jackson-core", "gson", "json",
                          "fastjson2", "json-simple", "json-smart", "moshi"])
        self.assertEqual(metrics, sorted(metrics, reverse=True))
        self.assertTrue(all(parser["family"].startswith("Jackson") for parser in parsers[:2]))
        self.assertTrue(parsers[2]["family"].startswith("Gson"))
        self.assertTrue(parsers[3]["family"].startswith("org.json"))
        self.assertTrue(parsers[4]["family"].startswith("fastjson2"))
        self.assertTrue(parsers[5]["family"].startswith("json-simple"))
        self.assertTrue(parsers[6]["family"].startswith("json-smart"))
        self.assertTrue(parsers[7]["family"].startswith("Moshi"))
        self.assertTrue(all(lead["status"] in {"unresolved", "promoted_to_verified"}
                            for lead in leads))
        self.assertEqual({lead["name"] for lead in leads
                          if lead["status"] == "promoted_to_verified"},
                         {"jackson-core", "json", "fastjson2", "json-simple", "json-smart", "moshi"})
        snapshot = read(BASE / "registry-snapshot.json")
        for parser in parsers:
            self.assertNotIn(parser["name"],
                             {lead["name"] for lead in leads if lead["status"] == "unresolved"})
            recorded = snapshot["popularity_metric"]["packages"][
                f"{parser['group']}:{parser['artifact']}"]
            self.assertEqual(recorded["summed_direct_dependent_count"], parser["popularity"]["value"])
        # Higher-adoption unresolved leads remain visible; rank is among verified paths.
        above = {lead["name"] for lead in leads if lead["status"] == "unresolved"
                 and lead["summed_direct_dependent_count"] > metrics[-1]}
        self.assertEqual(above, {"fastjson"})
        cell = read(BASE / "cell.json")
        self.assertEqual(sum(lead["status"] == "unresolved" for lead in leads),
                         cell["unresolved_documentation_leads"])
        self.assertEqual(len(parsers), cell["verified_third_party_count"])

    def test_control_receipts_match_catalog(self):
        for parser in read(BASE / "parsers.json"):
            with self.subTest(parser["name"]):
                self.check_receipt(parser)

    def check_receipt(self, parser):
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
        projects = {Path(parser["project"]).name for parser in read(BASE / "parsers.json")}
        self.assertEqual({Path(item["project"]).name for item in report["results"]}, projects)
        outputs = []
        for result in report["results"]:
            overlay = ROOT / "fuzzing/afl-native" / result["project"] / "verification.json"
            self.assertEqual(sha256(overlay.read_bytes()).hexdigest(), result["overlay_receipt_sha256"])
            self.assertTrue(result["pass"] and result["repeated_control_identical"])
            self.assertGreater(result["parser_feature_difference"], 0)
            self.assertGreater(result["afl_tuple_difference"], 0)
            outputs.append(result["differential_output"])
        self.assertEqual(outputs[0]["root"], "array")
        self.assertTrue(all(output == outputs[0] for output in outputs))

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
