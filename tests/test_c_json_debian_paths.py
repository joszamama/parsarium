"""C JSON paths found by the Debian source-name search keep pins, oracle, metric, family and feedback consistent."""

from hashlib import sha256
import gzip
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/c/json"
# Promoted Debian-search paths: slug -> (Debian source package, popcon sourcemax installations).
PATHS = {
    "json-glib": ("json-glib", 163249),
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


def popcon_rows() -> dict:
    archive = ROOT / "data/curation/popcon-sourcemax-by_inst.gz"
    rows = {}
    for line in gzip.decompress(archive.read_bytes()).decode().splitlines():
        parts = line.split()
        if not line.startswith("#") and len(parts) > 2 and parts[0].isdigit() and parts[2].isdigit():
            rows[parts[1]] = int(parts[2])
    return rows


class CJsonDebianPathsTest(unittest.TestCase):
    def test_search_is_recorded_against_the_hashed_snapshot(self):
        snapshot = read(BASE / "registry-snapshot.json")
        search = snapshot["debian_source_search"]
        archive = ROOT / search["local_snapshot"]
        self.assertEqual(sha256(archive.read_bytes()).hexdigest(), search["snapshot_sha256"])
        self.assertEqual(search["snapshot_sha256"], snapshot["adoption_metric"]["sha256"])
        rows = popcon_rows()
        names = sorted(name for name in rows if "json" in name.lower())
        self.assertEqual(sorted(hit["name"] for hit in search["hits"]), names)
        self.assertEqual((search["total"], search["unique_hits"]), (len(names), len(names)))
        classified = {row["name"] for row in search["c_json_classification"]}
        self.assertTrue({"json-glib", "libfastjson", "libjsonparser", "liblaxjson"} <= classified)
        self.assertEqual(sum(search["other_hits_by_category"].values()) + len(classified), len(names))
        extra = {row["name"]: row["inst"] for row in search["supplementary_exact_source_names"]["rows"]}
        self.assertEqual(extra["jq"], rows["jq"])
        self.assertIsNone(extra["parson"])

    def test_pins_agree(self):
        for slug in PATHS:
            project = ROOT / "projects/json/c" / slug
            manifest = read(project / "manifest.json")
            lock = read(project / "source-lock.json")[manifest["package"]]
            dockerfile = (project / "Dockerfile").read_text()
            self.assertEqual(manifest["release"], lock["release"], slug)
            self.assertEqual(manifest["source_sha256"], lock["source_sha256"], slug)
            for pinned in (lock["source_sha256"], lock["source"], manifest["base_image"]):
                self.assertIn(pinned, dockerfile, slug)
            self.assertEqual(manifest["afl_entrypoint"], "/work/parser-probe")

    def test_independent_oracle_matches_controls(self):
        for slug in PATHS:
            manifest = read(ROOT / "projects/json/c" / slug / "manifest.json")
            for control, digest, expected in (
                    (manifest["control"], manifest["control_sha256"], manifest["expected_output"]),
                    (manifest["differential_control"], manifest["differential_control_sha256"],
                     manifest["differential_expected_output"])):
                data = (ROOT / control).read_bytes()
                self.assertEqual(sha256(data).hexdigest(), digest)
                self.assertEqual(summarize(json.loads(data)), expected, (slug, control))

    def test_receipts_match_catalog(self):
        parsers = {item["name"]: item for item in read(BASE / "parsers.json")}
        records = {item["package"]: item for item in read(BASE / "verification.json")["third_party"]}
        for slug in PATHS:
            project = ROOT / "projects/json/c" / slug
            manifest = read(project / "manifest.json")
            receipt = read(project / "verification.json")
            record = records[slug]
            self.assertTrue(receipt["pass"] and record["pass"] and record["differential_pass"])
            self.assertEqual(receipt["output"], manifest["expected_output"])
            self.assertEqual(parsers[slug]["expected_output"], manifest["expected_output"])
            self.assertEqual(record["second_valid_output"], manifest["differential_expected_output"])
            self.assertEqual(record["parser_source_lines_covered"], receipt["parser_source_lines_covered"])
            self.assertGreater(receipt["format_specific_source_lines_covered"], 100, slug)
            for name, digest in receipt["project_file_sha256"].items():
                self.assertEqual(sha256((project / name).read_bytes()).hexdigest(), digest, (slug, name))

    def test_metric_matches_snapshot_and_rank_order(self):
        rows = popcon_rows()
        parsers = read(BASE / "parsers.json")
        values = [item["popularity"]["value"] for item in parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        ranking = (BASE / "ranking.md").read_text(encoding="utf-8")
        by_name = {item["name"]: item for item in parsers}
        for slug, (source, installs) in PATHS.items():
            popularity = by_name[slug]["popularity"]
            self.assertEqual(popularity["value"], installs)
            self.assertEqual(rows[source], installs)
            self.assertTrue(popularity["metric"].endswith(f"source package {source}"))
            rank = [item["name"] for item in parsers].index(slug) + 1
            self.assertIn(f"| {rank} | [", ranking)
            self.assertIn(f"| `{source}` | {installs:,} |", ranking)

    def test_families_are_stated(self):
        parsers = {item["name"]: item for item in read(BASE / "parsers.json")}
        self.assertIn("JsonScanner", parsers["json-glib"]["family"])
        families = [item["family"] for item in parsers.values()]
        self.assertEqual(len(families), len(set(families)))

    def test_leads_and_cell_counts(self):
        leads = {item["name"]: item for item in read(BASE / "leads.json")}
        for slug in PATHS:
            self.assertEqual(leads[slug]["status"], "resolved_verified_selected")
        self.assertEqual(leads["frozen"]["status"], "unresolved_failed_control")
        self.assertIn("636166e9", leads["frozen"]["reason"])
        self.assertEqual(leads["jsmn"]["status"], "not_eligible_tokenizer_only")
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(read(BASE / "parsers.json")))
        self.assertLessEqual(cell["verified_third_party_count"], cell["ceiling"])
        self.assertEqual(cell["unresolved_documentation_leads"],
                         sum(item["status"] == "unresolved" for item in leads.values()))

    def test_feedback_is_parser_scoped_stable_and_differential(self):
        report = {item["project"]: item for item in read(BASE / "afl-feedback.json")["results"]}
        for slug in PATHS:
            project = ROOT / "projects/json/c" / slug
            overlay = ROOT / "fuzzing/afl-native/json/c" / slug
            result = report[f"json/c/{slug}"]
            differential = read(overlay / "differential.json")
            receipt = read(overlay / "verification.json")
            self.assertEqual(sha256((overlay / "verification.json").read_bytes()).hexdigest(),
                             result["overlay_receipt_sha256"])
            self.assertEqual(sha256((overlay / "differential.json").read_bytes()).hexdigest(),
                             result["differential_receipt_sha256"])
            self.assertEqual(receipt["base_project_receipt_sha256"],
                             sha256((project / "verification.json").read_bytes()).hexdigest())
            self.assertEqual(differential["repeats_per_control"], 3)
            self.assertTrue(differential["repeated_feedback_identical"])
            self.assertEqual(differential["dom_oracle"], "python_json_loads_order_and_number_kind_preserving")
            self.assertEqual(result["control_afl_tuples"], receipt["feedback_edges"])
            self.assertGreater(result["afl_tuple_difference"], 0)
            self.assertGreater(result["source_line_difference"], 0)
            objects = differential["afl_instrumented_objects"]
            self.assertTrue(objects and not any("parser-probe" in name for name in objects), slug)
            self.assertEqual(differential["allowlist_entries"],
                             (project / "afl-allowlist.txt").read_text().split())


if __name__ == "__main__":
    unittest.main()
