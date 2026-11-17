"""The C++ Boost.JSON path keeps its pins, exact oracle, metric labels and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/cpp/json"
PACKAGE = "Boost.JSON"
PROJECT = ROOT / "projects/json/cpp/boost-json"
OVERLAY = ROOT / "fuzzing/afl-native/json/cpp/boost-json"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def summarize(tree: object) -> dict:
    counts = {"arrays": 0, "objects": 0, "booleans": 0, "nulls": 0, "max_depth": 0}
    numbers, strings = [], []

    def walk(value: object, depth: int) -> None:
        if isinstance(value, dict):
            counts["objects"] += 1
            counts["max_depth"] = max(counts["max_depth"], depth)
            for child in value.values(): walk(child, depth + 1)
        elif isinstance(value, list):
            counts["arrays"] += 1
            counts["max_depth"] = max(counts["max_depth"], depth)
            for child in value: walk(child, depth + 1)
        elif value is None: counts["nulls"] += 1
        elif isinstance(value, bool): counts["booleans"] += 1
        elif isinstance(value, (int, float)): numbers.append(value)
        elif isinstance(value, str): strings.append(value)

    walk(tree, 1)
    result = {**counts, "numbers": sorted(numbers), "strings": sorted(strings),
              "root": "object" if isinstance(tree, dict) else "array"}
    if isinstance(tree, dict): result["top_level_keys"] = sorted(tree)
    else: result["top_level_items"] = len(tree)
    return result


class CppJsonBoostPilotTest(unittest.TestCase):
    def test_pins_agree(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual((manifest["release"], lock["release"]), ("1.92.0", "1.92.0"))
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        for pinned in (lock["source_sha256"], lock["source_url"], manifest["base_image"]):
            self.assertIn(pinned, dockerfile)
        # Only Boost.JSON's own headers sit under the counted coverage prefix.
        self.assertIn("mv /work/boost/boost/json /work/boost/boost/json.hpp /work/source/boost/", dockerfile)
        self.assertIn("json::parse(", (PROJECT / "harness.cpp").read_text())

    def test_independent_oracle_matches_controls(self):
        manifest = read(PROJECT / "manifest.json")
        for control, digest, expected in (
                (manifest["control"], manifest["control_sha256"], manifest["expected_output"]),
                (manifest["differential_control"], manifest["differential_control_sha256"],
                 manifest["differential_expected_output"])):
            data = (ROOT / control).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), digest)
            self.assertEqual(summarize(json.loads(data)), expected, control)

    def test_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        record, = [item for item in read(BASE / "verification.json")["third_party"]
                   if item["package"] == PACKAGE]
        self.assertTrue(receipt["pass"] and record["pass"] and record["differential_pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        self.assertEqual(record["output"], manifest["expected_output"])
        self.assertEqual(record["second_valid_output"], manifest["differential_expected_output"])
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertEqual(record["parser_source_lines_covered"], receipt["parser_source_lines_covered"])

    def test_metric_is_unranked_with_labeled_fallback(self):
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        popularity = parser["popularity"]
        self.assertIsNone(popularity["value"])
        self.assertFalse(popularity["ranked"])
        self.assertEqual(popularity["fallback"]["value"], 1749)
        self.assertEqual(popularity["fallback"]["binary_package"], "libboost-json-dev")
        snapshot = read(BASE / "registry-snapshot.json")
        rows = {row["name"]: row["inst"] for row in snapshot["boost_json_binary_packages"]["rows"]}
        self.assertEqual(rows["libboost-json-dev"], 1749)
        self.assertEqual(rows["libboost-json1.83.0"], popularity["runtime_package_installs"]["libboost-json1.83.0"])
        self.assertEqual(popularity["fallback"]["source_sha256"], snapshot["sources"]["binary_by_inst"]["sha256"])
        boost, = [row for row in snapshot["multi_purpose_sources_with_json_modules"]["rows"]
                  if row["name"] == "boost1.83"]
        self.assertIn(f"{boost['inst']:,}", popularity["unranked_reason"])
        ranking = (BASE / "ranking.md").read_text(encoding="utf-8")
        self.assertIn("| — | [Boost.JSON]", ranking)

    def test_family_is_independent_and_lead_resolved(self):
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        self.assertEqual(parser["family"], "Boost.JSON basic_parser")
        families = [item["family"] for item in read(BASE / "parsers.json")]
        self.assertEqual(families.count("Boost.JSON basic_parser"), 1)
        record, = [item for item in read(BASE / "verification.json")["third_party"]
                   if item["package"] == PACKAGE]
        self.assertEqual(record["family_status"], "independent")
        leads = {lead["name"] for lead in read(BASE / "leads.json")}
        self.assertNotIn(PACKAGE, leads)
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(read(BASE / "parsers.json")))
        self.assertEqual(cell["unresolved_documentation_leads"], len(leads))

    def test_feedback_is_stable_and_differential(self):
        report = read(BASE / "afl-feedback.json")
        result, = [item for item in report["results"] if item["project"] == "json/cpp/boost-json"]
        differential = read(OVERLAY / "differential.json")
        overlay = read(OVERLAY / "verification.json")
        self.assertEqual(sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
                         result["overlay_receipt_sha256"])
        self.assertEqual(sha256((OVERLAY / "differential.json").read_bytes()).hexdigest(),
                         result["differential_receipt_sha256"])
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertTrue(result["pass"] and result["repeated_control_identical"])
        self.assertEqual(differential["repeats_per_control"], 2)
        self.assertEqual(differential["second_case_kind"], "valid_control")
        self.assertEqual(differential["dom_oracle"], "python_json_loads_order_and_number_kind_preserving")
        self.assertGreater(result["source_line_difference"], 0)
        self.assertGreater(result["afl_tuple_difference"], 0)
        self.assertEqual(result["control_afl_tuples"], overlay["feedback_edges"])
        self.assertTrue(all(name.startswith("boost/json") for name in
                            {**differential["first_only_lines_by_file"],
                             **differential["second_only_lines_by_file"]}))


if __name__ == "__main__":
    unittest.main()
