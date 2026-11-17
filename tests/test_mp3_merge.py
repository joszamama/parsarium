"""The single MP3 format keeps the ten most-adopted paths of both former MP3 cells."""

import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import format_registry  # noqa: E402

ECOSYSTEMS = ("c", "cpp", "go", "java", "javascript", "python", "rust", "php")
FRESH = {"c": ("popularity_metric", "install_on_request_365d", "install_on_request_365d"),
         "go": ("popularity_metric", "imported_by_packages", "imported_by"),
         "javascript": ("download_metric", "downloads", "downloads"),
         "python": ("download_metric", "downloads", "downloads")}


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


class Mp3MergeTest(unittest.TestCase):
    def setUp(self):
        self.record = read(ROOT / "data/curation/mp3-merge.json")
        self.plan = {(c["ecosystem"], c["format"]): c for c in read(ROOT / "data/curation/plan.json")["cells"]}

    def test_registry_has_one_active_mp3_format_with_a_project_alias(self):
        self.assertIn("mp3", format_registry.ACTIVE_FORMATS)
        self.assertNotIn("mp3_id3v2", format_registry.FORMAT_BY_ID)
        self.assertEqual(format_registry.catalog_format("mp3_id3v2"), "mp3")
        self.assertEqual(format_registry.resolve_data_path("data/go/mp3_id3v2/parsers.json"),
                         "data/go/mp3/parsers.json")
        cells = read(ROOT / "data/cells.json")["cells"]
        self.assertEqual(sum(c["format"] == "mp3" for c in cells), 8)
        self.assertFalse(any(c["format"] == "mp3_id3v2" for c in cells))
        self.assertFalse(any(c["format"] == "mp3" for c in read(ROOT / "data/pilot-cells.json")["cells"]))

    def test_each_cell_keeps_the_planned_top_ten(self):
        by_eco = {c["ecosystem"]: c for c in self.record["cells"]}
        self.assertEqual(set(by_eco), set(ECOSYSTEMS))
        for eco in ECOSYSTEMS:
            parsers = read(ROOT / f"data/{eco}/mp3/parsers.json")
            names = [p["name"] for p in parsers]
            plan = self.plan[(eco, "mp3")]
            self.assertEqual(names, [item["name"] for item in plan["selected"]], eco)
            self.assertEqual(names, [item["name"] for item in by_eco[eco]["kept"]], eco)
            self.assertLessEqual(len(names), 10)
            self.assertEqual(read(ROOT / f"data/{eco}/mp3/cell.json")["verified_third_party_count"], len(names))
            for parser in parsers:
                project = ROOT / parser["project"]
                manifest = read(project / "manifest.json")
                self.assertEqual(manifest["package"], parser["name"])
                expected_dir = "mp3_id3v2" if parser["control_kind"] == "id3v2_tagged" else "mp3"
                self.assertEqual(Path(parser["project"]).parts[1], expected_dir)
                self.assertEqual(manifest["control"], parser["control"])
                self.assertTrue(read(project / "verification.json")["pass"])

    def test_removed_paths_are_gone_and_recorded_as_leads(self):
        for cell in self.record["cells"]:
            eco = cell["ecosystem"]
            leads = {lead["name"]: lead for lead in read(ROOT / f"data/{eco}/mp3/leads.json")}
            selected = {p["name"] for p in read(ROOT / f"data/{eco}/mp3/parsers.json")}
            for removed in cell["removed"]:
                self.assertNotIn(removed["name"], selected)
                self.assertEqual(leads[removed["name"]]["status"], "removed_mp3_merge_below_top10")
            for duplicate in cell["duplicates"]:
                self.assertIn(duplicate["name"], selected)
                self.assertTrue((ROOT / duplicate["kept_project"] / "manifest.json").is_file())
        for project in self.record["removed_projects"]:
            fmt, eco, slug = Path(project).parts[1:4]
            self.assertFalse((ROOT / project).exists(), project)
            self.assertFalse((ROOT / "fuzzing/afl-native" / fmt / eco / slug).exists(), project)

    def test_fresh_capture_is_the_ranking_value(self):
        for eco, (block, field, fresh_field) in FRESH.items():
            snapshot = read(ROOT / f"data/{eco}/mp3/registry-snapshot.json")
            fresh = snapshot["merged_mp3_ranking_2026_11_17"]["packages"]
            for item in self.plan[(eco, "mp3")]["selected"]:
                value = snapshot[block]["packages"][item["name"]][field]
                self.assertEqual(value, fresh[item["name"]][fresh_field], (eco, item["name"]))
                if item["selection"] == "primary_metric":
                    self.assertEqual(item["metric"], value)

    def test_pinned_manifest_paths_still_resolve(self):
        for manifest_path in sorted((ROOT / "projects/mp3_id3v2").glob("*/*/manifest.json")):
            manifest = read(manifest_path)
            for key in ("catalog_parser", "source_lock", "standard_inventory", "underlying_source_lock"):
                value = manifest.get(key)
                if isinstance(value, str) and value.startswith("data/"):
                    self.assertTrue((ROOT / value).is_file(), (manifest_path, key))
                    self.assertTrue((ROOT / format_registry.resolve_data_path(value)).is_file())


if __name__ == "__main__":
    unittest.main()
