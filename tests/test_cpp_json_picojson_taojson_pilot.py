"""The C++ PicoJSON and taoJSON paths keep pins, key-order limit, weak metrics and feedback consistent."""

from hashlib import sha256
import gzip
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/cpp/json"
PATHS = {
    # package: (slug, Debian source, sourcemax installs, rank, file-only allowlist map size)
    "PicoJSON": ("picojson", "picojson", 16, 6, 145),
    "taoJSON": ("tao-json", "tao-json", 2, 8, 834),
}


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


class CppJsonPicoTaoPilotTest(unittest.TestCase):
    def test_pins_agree(self):
        for package, (slug, *_rest) in PATHS.items():
            project = ROOT / "projects/json/cpp" / slug
            manifest = read(project / "manifest.json")
            lock = read(project / "source-lock.json")
            dockerfile = (project / "Dockerfile").read_text()
            self.assertEqual(manifest["release"], lock[package]["release"])
            self.assertEqual(manifest["source_sha256"], lock[package]["source_sha256"])
            for item in lock.values():
                self.assertIn(item["source_sha256"], dockerfile)
                self.assertIn(item["source_url"], dockerfile)
            self.assertIn(manifest["base_image"], dockerfile)
        tao = read(ROOT / "projects/json/cpp/tao-json/source-lock.json")
        self.assertEqual(tao["PEGTL"]["release"], "3.2.6")
        self.assertTrue(tao["taoJSON"]["upstream_prerelease"])
        # Without PICOJSON_USE_INT64, picojson stores every number as double.
        self.assertIn("-DPICOJSON_USE_INT64", (ROOT / "projects/json/cpp/picojson/build.sh").read_text())

    def test_independent_oracle_matches_controls(self):
        for package, (slug, *_rest) in PATHS.items():
            manifest = read(ROOT / "projects/json/cpp" / slug / "manifest.json")
            for control, digest, expected in (
                    (manifest["control"], manifest["control_sha256"], manifest["expected_output"]),
                    (manifest["differential_control"], manifest["differential_control_sha256"],
                     manifest["differential_expected_output"])):
                data = (ROOT / control).read_bytes()
                self.assertEqual(sha256(data).hexdigest(), digest)
                self.assertEqual(summarize(json.loads(data)), expected, (package, control))
            # The key-order limit is stated where the oracle is defined.
            self.assertIn("std::map", manifest["oracle"])
            self.assertIn("sorted key order", manifest["oracle"])

    def test_receipt_matches_catalog(self):
        parsers = read(BASE / "parsers.json")
        records = read(BASE / "verification.json")["third_party"]
        for package, (slug, *_rest) in PATHS.items():
            project = ROOT / "projects/json/cpp" / slug
            manifest = read(project / "manifest.json")
            receipt = read(project / "verification.json")
            parser, = [item for item in parsers if item["name"] == package]
            record, = [item for item in records if item["package"] == package]
            self.assertTrue(receipt["pass"] and record["pass"] and record["differential_pass"])
            self.assertIs(record["object_key_order_checked"], False)
            self.assertIn("key order is not preserved", parser["scope"])
            for observed in (receipt["output"], parser["expected_output"], record["output"]):
                self.assertEqual(observed, manifest["expected_output"])
            self.assertEqual(record["second_valid_output"], manifest["differential_expected_output"])
            for name, digest in receipt["project_file_sha256"].items():
                self.assertEqual(sha256((project / name).read_bytes()).hexdigest(), digest, name)
            self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        tao = read(ROOT / "projects/json/cpp/tao-json/verification.json")
        self.assertGreater(tao["underlying_source_lines_covered"], 0)

    def test_weak_primary_metric_matches_snapshot_and_rank(self):
        parsers = read(BASE / "parsers.json")
        snapshot = read(BASE / "registry-snapshot.json")
        sources = {row["name"]: row for row in snapshot["search"][0]["hits"]}
        archive = ROOT / "data/curation/popcon-sourcemax-by_inst.gz"
        self.assertEqual(sha256(archive.read_bytes()).hexdigest(),
                         snapshot["sources"]["sourcemax_by_inst"]["sha256"])
        rows = [line.split()[1:3] for line in gzip.decompress(archive.read_bytes()).decode().splitlines()
                if not line.startswith("#") and len(line.split()) > 2]
        ranking = (BASE / "ranking.md").read_text(encoding="utf-8")
        for package, (slug, source, installs, rank, _) in PATHS.items():
            parser, = [item for item in parsers if item["name"] == package]
            self.assertEqual(parser["popularity"]["value"], installs)
            self.assertIn("weak", parser["popularity"]["qualification"].lower())
            self.assertEqual(sources[source]["inst"], installs)
            self.assertIn([source, str(installs)], rows)
            self.assertIn(f"| {rank} | [{package}]", ranking)
        binaries = {row["name"]: row["inst"] for row in snapshot["binary_packages"]}
        self.assertEqual(binaries["picojson-dev"], 16)
        primary = parsers[0]["popularity"]["metric"]
        ranked = [item["popularity"]["value"] for item in parsers
                  if item["popularity"]["metric"] == primary
                  and isinstance(item["popularity"].get("value"), int)]
        self.assertEqual(ranked, sorted(ranked, reverse=True))
        self.assertEqual(len(ranked), 8)

    def test_cell_is_at_ceiling_and_leads_resolved(self):
        parsers = read(BASE / "parsers.json")
        cell = read(BASE / "cell.json")
        leads = read(BASE / "leads.json")
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(len(parsers), cell["ceiling"])
        self.assertEqual(cell["unresolved_documentation_leads"],
                         sum(item["status"] == "unresolved" for item in leads))
        for package in PATHS:
            lead, = [item for item in leads if item["name"] == package]
            self.assertEqual(lead["status"], "resolved_verified_selected")
            parser, = [item for item in parsers if item["name"] == package]
            self.assertEqual([item["family"] for item in parsers].count(parser["family"]), 1)
        rescan = read(BASE / "registry-snapshot.json")["cpp_json_rescan_2026_11_17"]["rows"]
        self.assertTrue(all(row["status"].startswith("excluded:") for row in rescan))
        self.assertNotIn("[PicoJSON](https://github.com/kazuho/picojson) | 16 | unavailable | Not control-tested",
                         (BASE / "ranking.md").read_text(encoding="utf-8"))

    def test_feedback_is_stable_and_differential(self):
        report = read(BASE / "afl-feedback.json")
        for package, (slug, _source, _installs, _rank, file_only_sites) in PATHS.items():
            project = ROOT / "projects/json/cpp" / slug
            overlay_dir = ROOT / "fuzzing/afl-native/json/cpp" / slug
            result, = [item for item in report["results"] if item["project"] == f"json/cpp/{slug}"]
            differential = read(overlay_dir / "differential.json")
            overlay = read(overlay_dir / "verification.json")
            self.assertEqual(sha256((overlay_dir / "verification.json").read_bytes()).hexdigest(),
                             result["overlay_receipt_sha256"])
            self.assertEqual(sha256((overlay_dir / "differential.json").read_bytes()).hexdigest(),
                             result["differential_receipt_sha256"])
            self.assertEqual(overlay["base_project_receipt_sha256"],
                             sha256((project / "verification.json").read_bytes()).hexdigest())
            self.assertTrue(result["pass"] and result["repeated_control_identical"])
            self.assertEqual(differential["repeats_per_control"], 3)
            self.assertEqual(differential["second_case_kind"], "valid_control")
            self.assertGreater(result["source_line_difference"], 0)
            self.assertGreater(result["afl_tuple_difference"], 10)
            self.assertEqual(result["control_afl_tuples"], overlay["feedback_edges"])
            # Function-scoped entries instrument parser templates inlined into the probe.
            self.assertTrue(any(entry.startswith("fun:") for entry in differential["allowlist_entries"]))
            self.assertGreater(overlay["afl_map_size"], file_only_sites)
        self.assertEqual(report["projects_total"], 10)
        self.assertEqual(report["projects_passed"], 10)


if __name__ == "__main__":
    unittest.main()
