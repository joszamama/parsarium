"""The C++ jsoncons path keeps its pins, ordered oracle, weak metric label and feedback consistent."""

from hashlib import sha256
import gzip
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/cpp/json"
PACKAGE = "jsoncons"
PROJECT = ROOT / "projects/json/cpp/jsoncons"
OVERLAY = ROOT / "fuzzing/afl-native/json/cpp/jsoncons"


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


class CppJsonJsonconsPilotTest(unittest.TestCase):
    def test_pins_agree(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual((manifest["release"], lock["release"]), ("1.10.0", "1.10.0"))
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        for pinned in (lock["source_sha256"], lock["source_url"], manifest["base_image"]):
            self.assertIn(pinned, dockerfile)
        # The ordered ojson type keeps control key order; the default json type sorts keys.
        for name in ("harness.cpp", "parser-probe.cpp"):
            text = (PROJECT / name).read_text()
            self.assertIn("jsoncons::ojson::parse(", text)
            self.assertNotIn("jsoncons::json::parse(", text)
        allowlist = (PROJECT / "afl-allowlist.txt").read_text().split()
        self.assertIn("fun:_ZN8jsoncons17basic_json_parser*", allowlist)

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
        self.assertEqual(receipt["format_specific_source_lines_covered"], 726)
        self.assertEqual(record["parser_source_lines_covered"], receipt["parser_source_lines_covered"])

    def test_weak_primary_metric_matches_snapshot_and_rank(self):
        parsers = read(BASE / "parsers.json")
        parser, = [item for item in parsers if item["name"] == PACKAGE]
        popularity = parser["popularity"]
        self.assertEqual(popularity["value"], 3)
        self.assertIn("weak", popularity["qualification"])
        snapshot = read(BASE / "registry-snapshot.json")
        sources = {row["name"]: row["inst"] for row in snapshot["search"][0]["hits"]}
        self.assertEqual(sources["jsoncons"], 3)
        binaries = {row["name"]: row["inst"] for row in snapshot["binary_packages"]}
        self.assertEqual(binaries["libjsoncons-dev"], popularity["dev_package_installs"]["libjsoncons-dev"])
        archive = ROOT / "data/curation/popcon-sourcemax-by_inst.gz"
        self.assertEqual(sha256(archive.read_bytes()).hexdigest(),
                         snapshot["sources"]["sourcemax_by_inst"]["sha256"])
        rows = [line.split() for line in gzip.decompress(archive.read_bytes()).decode().splitlines()
                if not line.startswith("#")]
        self.assertIn(["jsoncons", "3"], [row[1:3] for row in rows if len(row) > 2])
        ranked = [item["popularity"]["value"] for item in parsers
                  if item["popularity"]["metric"] == popularity["metric"]
                  and isinstance(item["popularity"].get("value"), int)]
        self.assertEqual(ranked, sorted(ranked, reverse=True))
        self.assertIn("| 8 | [jsoncons]", (BASE / "ranking.md").read_text(encoding="utf-8"))

    def test_family_is_independent_and_lead_resolved(self):
        parsers = read(BASE / "parsers.json")
        parser, = [item for item in parsers if item["name"] == PACKAGE]
        self.assertEqual(parser["family"], "jsoncons own basic_json_parser")
        self.assertEqual([item["family"] for item in parsers].count(parser["family"]), 1)
        leads = read(BASE / "leads.json")
        lead, = [item for item in leads if item["name"] == PACKAGE]
        self.assertEqual(lead["status"], "resolved_verified_selected")
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(cell["unresolved_documentation_leads"],
                         sum(item["status"] == "unresolved" for item in leads))
        self.assertNotIn("[jsoncons](https://github.com/danielaparker/jsoncons) | 3 | 3 | Not control-tested",
                         (BASE / "ranking.md").read_text(encoding="utf-8"))

    def test_feedback_is_stable_and_differential(self):
        report = read(BASE / "afl-feedback.json")
        result, = [item for item in report["results"] if item["project"] == "json/cpp/jsoncons"]
        differential = read(OVERLAY / "differential.json")
        overlay = read(OVERLAY / "verification.json")
        self.assertEqual(sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
                         result["overlay_receipt_sha256"])
        self.assertEqual(sha256((OVERLAY / "differential.json").read_bytes()).hexdigest(),
                         result["differential_receipt_sha256"])
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertTrue(result["pass"] and result["repeated_control_identical"])
        self.assertEqual(differential["repeats_per_control"], 3)
        self.assertEqual(differential["second_case_kind"], "valid_control")
        self.assertEqual(differential["dom_oracle"], "python_json_loads_order_and_number_kind_preserving")
        self.assertGreater(result["source_line_difference"], 0)
        # A file-only allowlist yielded a 60-site map and one differing tuple; the
        # function-scoped allowlist instruments the basic_json_parser methods.
        self.assertGreater(overlay["afl_map_size"], 1000)
        self.assertGreater(result["afl_tuple_difference"], 10)
        self.assertEqual(result["control_afl_tuples"], overlay["feedback_edges"])


if __name__ == "__main__":
    unittest.main()
