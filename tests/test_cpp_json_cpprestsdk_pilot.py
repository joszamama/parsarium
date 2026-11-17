"""The C++ cpprestsdk JSON path keeps its pin, ordered-tree oracle, metric lookup and scoped feedback consistent."""

from hashlib import sha256
import gzip
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/cpp/json"
PROJECT = ROOT / "projects/json/cpp/cpprestsdk"
OVERLAY = ROOT / "fuzzing/afl-native/json/cpp/cpprestsdk"
JSON_UNITS = ("json.cpp", "json_parsing.cpp", "json_serialization.cpp")


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


class CppJsonCpprestsdkPilotTest(unittest.TestCase):
    def test_pin_and_build_scope(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")["cpprestsdk"]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual(manifest["release"], lock["release"])
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        self.assertIn(lock["source_sha256"], dockerfile)
        self.assertIn(lock["source_url"], dockerfile)
        self.assertIn(manifest["base_image"], dockerfile)
        self.assertEqual(lock["license"], "MIT")
        build = (PROJECT / "build.sh").read_text()
        for unit in JSON_UNITS:
            self.assertIn(f"/Release/src/json/{unit}", build)
        # The shim replaces the HTTP/websocket precompiled header; it must not pull Boost or pplx.
        includes = [line for line in (PROJECT / "stdafx.h").read_text().splitlines()
                    if line.startswith("#include")]
        self.assertFalse([line for line in includes if "boost" in line.lower() or "pplx" in line])
        self.assertIn('#include "cpprest/json.h"', includes)

    def test_ordered_oracle_matches_controls(self):
        manifest = read(PROJECT / "manifest.json")
        for control, digest, expected in (
                (manifest["control"], manifest["control_sha256"], manifest["expected_output"]),
                (manifest["differential_control"], manifest["differential_control_sha256"],
                 manifest["differential_expected_output"])):
            data = (ROOT / control).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), digest)
            self.assertEqual(summarize(json.loads(data)), expected, control)
        # Without keep_object_element_order(true) cpprest sorts object members by key.
        for name in ("harness.cpp", "parser-probe.cpp"):
            self.assertIn("web::json::keep_object_element_order(true)", (PROJECT / name).read_text())
        self.assertIn("preserving object member order", manifest["oracle"])

    def test_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "cpprestsdk"]
        record, = [item for item in read(BASE / "verification.json")["third_party"]
                   if item["package"] == "cpprestsdk"]
        self.assertTrue(receipt["pass"] and record["pass"] and record["differential_pass"])
        for observed in (receipt["output"], parser["expected_output"], record["output"]):
            self.assertEqual(observed, manifest["expected_output"])
        self.assertEqual(record["second_valid_output"], manifest["differential_expected_output"])
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        self.assertEqual(receipt["parser_source_files"], len(JSON_UNITS))
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertEqual(record["parser_source_lines_covered"], receipt["parser_source_lines_covered"])

    def test_primary_metric_from_supplementary_lookup(self):
        parsers = read(BASE / "parsers.json")
        snapshot = read(BASE / "registry-snapshot.json")
        lookup = snapshot["supplementary_named_source_lookups_tenth_slot"]
        archive = ROOT / "data/curation/popcon-sourcemax-by_inst.gz"
        self.assertEqual(sha256(archive.read_bytes()).hexdigest(), lookup["snapshot_sha256"])
        self.assertEqual(lookup["snapshot_sha256"], snapshot["sources"]["sourcemax_by_inst"]["sha256"])
        rows = {line.split()[1]: line.split() for line in gzip.decompress(archive.read_bytes()).decode().splitlines()
                if not line.startswith("#") and len(line.split()) > 6}
        for row in lookup["rows"]:
            self.assertEqual(rows[row["name"]][:3], [str(row["rank"]), row["name"], str(row["inst"])])
        self.assertNotIn("cpprest", {hit["name"] for hit in snapshot["search"][0]["hits"]})
        parser, = [item for item in parsers if item["name"] == "cpprestsdk"]
        self.assertEqual(parser["popularity"]["value"], int(rows["cpprest"][2]))
        self.assertIn("not JSON-specific", parser["popularity"]["qualification"])
        self.assertIn("| 5 | [cpprestsdk]", (BASE / "ranking.md").read_text(encoding="utf-8"))
        primary = parsers[0]["popularity"]["metric"]
        ranked = [item["popularity"]["value"] for item in parsers
                  if item["popularity"]["metric"] == primary
                  and isinstance(item["popularity"].get("value"), int)]
        self.assertEqual(ranked, sorted(ranked, reverse=True))
        self.assertEqual([item["family"] for item in parsers].count(parser["family"]), 1)
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(len(parsers), cell["ceiling"])

    def test_feedback_is_scoped_stable_and_differential(self):
        report = read(BASE / "afl-feedback.json")
        result, = [item for item in report["results"] if item["project"] == "json/cpp/cpprestsdk"]
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
        self.assertGreater(result["source_line_difference"], 0)
        self.assertGreater(result["afl_tuple_difference"], 0)
        self.assertEqual(result["control_afl_tuples"], overlay["feedback_edges"])
        self.assertEqual(differential["allowlist_entries"],
                         [f"src:*/Release/src/json/{unit}" for unit in JSON_UNITS])
        self.assertEqual(differential["instrumented_objects_nm_checked"],
                         [unit.replace(".cpp", ".o") for unit in JSON_UNITS])
        self.assertIn("test \"$instrumented\" = 'json.o json_parsing.o json_serialization.o '",
                      (PROJECT / "build.sh").read_text())


if __name__ == "__main__":
    unittest.main()
