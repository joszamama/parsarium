"""C TOML pilot paths keep pins, typed-tree controls, star-fallback metric, family and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/c/toml"
# Promoted paths: slug -> (parser source file inside the archive, GitHub stargazers from the
# round_6_star_fallback capture in the registry snapshot).
PATHS = {
    "tomlc17": ("src/tomlc17.c", 201),
}


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class CTomlPathsTest(unittest.TestCase):
    def test_pins_agree(self):
        for slug in PATHS:
            project = ROOT / "projects/toml/c" / slug
            manifest = read(project / "manifest.json")
            lock = read(project / "source-lock.json")[manifest["package"]]
            dockerfile = (project / "Dockerfile").read_text()
            self.assertEqual((manifest["format"], manifest["ecosystem"]), ("toml", "c"))
            self.assertEqual(manifest["release"], lock["release"], slug)
            self.assertEqual(manifest["source_sha256"], lock["source_sha256"], slug)
            self.assertEqual(len(lock["source_sha256"]), 64)
            for pinned in (lock["source_sha256"], lock["source"], manifest["base_image"]):
                self.assertIn(pinned, dockerfile, slug)
            self.assertIn("MIT", lock["license"])
            self.assertEqual(manifest["afl_entrypoint"], "/work/parser-probe")

    def test_controls_and_expected_trees(self):
        for slug in PATHS:
            manifest = read(ROOT / "projects/toml/c" / slug / "manifest.json")
            for control, digest, expected in (
                    (manifest["control"], manifest["control_sha256"], manifest["expected_output"]),
                    (manifest["differential_control"], manifest["differential_control_sha256"],
                     manifest["differential_expected_output"])):
                self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)
                tree = read(ROOT / control.replace(".toml", ".expected.json"))
                self.assertEqual(expected, tree, (slug, control))
            self.assertEqual(manifest["control"], "controls/toml/service-config.toml")
            self.assertEqual(manifest["differential_control"], "controls/toml/typed-scalars.toml")

    def test_receipts_match_catalog(self):
        parsers = {item["name"]: item for item in read(BASE / "parsers.json")}
        records = {item["package"]: item for item in read(BASE / "verification.json")["third_party"]}
        self.assertEqual(set(parsers), set(PATHS))
        for slug, (source_file, _) in PATHS.items():
            project = ROOT / "projects/toml/c" / slug
            manifest = read(project / "manifest.json")
            receipt = read(project / "verification.json")
            record = records[slug]
            self.assertTrue(receipt["pass"] and receipt["fuzz_engine_smoke_pass"])
            self.assertTrue(record["pass"] and record["differential_pass"])
            self.assertEqual(receipt["manifest"], f"projects/toml/c/{slug}/manifest.json")
            self.assertEqual(receipt["output"], manifest["expected_output"])
            self.assertEqual(parsers[slug]["expected_output"], manifest["expected_output"])
            self.assertEqual(record["output"], manifest["expected_output"])
            self.assertEqual(record["second_valid_output"], manifest["differential_expected_output"])
            self.assertEqual(parsers[slug]["version"], manifest["release"])
            self.assertEqual(record["version"], manifest["release"])
            self.assertEqual(record["parser_source_lines_covered"], receipt["parser_source_lines_covered"])
            self.assertTrue(manifest["format_specific_coverage_file_suffix"].endswith(source_file))
            self.assertGreater(receipt["format_specific_source_lines_covered"], 100, slug)
            for name, digest in receipt["project_file_sha256"].items():
                self.assertEqual(sha256((project / name).read_bytes()).hexdigest(), digest, (slug, name))

    def test_star_fallback_metric_and_rank_order(self):
        parsers = read(BASE / "parsers.json")
        snapshot = read(BASE / "registry-snapshot.json")
        captured = snapshot["round_6_star_fallback"]["repositories"]
        values = [item["supplemental_metric"]["value"] for item in parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        ranking = (BASE / "ranking.md").read_text(encoding="utf-8")
        self.assertIn("| Rank | Package | Release | Metric | Parsed scope | Parser family |", ranking)
        for rank, item in enumerate(parsers, 1):
            stars = PATHS[item["name"]][1]
            self.assertIsNone(item["metric"]["value"])
            self.assertIs(item["metric"]["ranked"], False)
            self.assertEqual(item["selection"], "supplemental")
            metric = item["supplemental_metric"]
            self.assertEqual(metric["value"], stars)
            self.assertGreaterEqual(stars, 100)
            self.assertEqual(metric["rank"], rank)
            self.assertEqual(metric["name"],
                             "GitHub stars (secondary, repository interest, not downloads)")
            repo = metric["repository"].removeprefix("https://github.com/")
            self.assertEqual(captured[repo]["stargazers_count"], stars)
            self.assertEqual(captured[repo]["response_sha256"], metric["response_sha256"])
            self.assertIn(metric["release_tag"], read(ROOT / "projects/toml/c" / item["name"]
                                                      / "source-lock.json")[item["name"]]["tag"])
            self.assertIn(f"| {rank} | [{item['name']}](", ranking)
        self.assertEqual(snapshot["search"][0]["query"], "toml")

    def test_families_are_stated(self):
        parsers = {item["name"]: item for item in read(BASE / "parsers.json")}
        self.assertIn("separate rewrite", parsers["tomlc17"]["family_note"])
        leads = {item["name"]: item for item in read(BASE / "leads.json")["leads"]}
        self.assertIn("tomlc99 family", leads["toml-c"]["family"])

    def test_leads_and_cell_counts(self):
        leads = {item["name"]: item for item in read(BASE / "leads.json")["leads"]}
        self.assertFalse(set(leads) & set(PATHS))
        self.assertEqual(leads["tomlc99"]["status"], "unresolved_control_failed")
        self.assertIn("expect hex char", leads["tomlc99"]["evidence"]["error"])
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(read(BASE / "parsers.json")))
        self.assertLessEqual(cell["verified_third_party_count"], cell["ceiling"])
        self.assertEqual(cell["unresolved_documentation_leads"],
                         sum(item["status"].startswith("unresolved") for item in leads.values()))
        self.assertEqual(len(cell["third_party_control_results"]), len(PATHS))

    def test_feedback_is_parser_scoped_stable_and_differential(self):
        report = {item["project"]: item for item in read(BASE / "afl-feedback.json")["results"]}
        for slug, (source_file, _) in PATHS.items():
            project = ROOT / "projects/toml/c" / slug
            overlay = ROOT / "fuzzing/afl-native/toml/c" / slug
            result = report[f"toml/c/{slug}"]
            differential = read(overlay / "differential.json")
            receipt = read(overlay / "verification.json")
            self.assertEqual(sha256((overlay / "verification.json").read_bytes()).hexdigest(),
                             result["overlay_receipt_sha256"])
            self.assertEqual(sha256((overlay / "verification.json").read_bytes()).hexdigest(),
                             differential["overlay_receipt_sha256"])
            self.assertEqual(sha256((overlay / "differential.json").read_bytes()).hexdigest(),
                             result["differential_receipt_sha256"])
            base_sha = sha256((project / "verification.json").read_bytes()).hexdigest()
            self.assertEqual(receipt["base_project_receipt_sha256"], base_sha)
            self.assertEqual(differential["base_project_receipt_sha256"], base_sha)
            self.assertTrue(receipt["pass"])
            self.assertGreaterEqual(differential["repeats_per_control"], 3)
            self.assertTrue(differential["repeated_feedback_identical"])
            self.assertEqual(result["control_afl_tuples"], receipt["feedback_edges"])
            self.assertEqual(differential["first_afl_tuples"], receipt["feedback_edges"])
            self.assertGreaterEqual(differential["afl_tuple_difference"], 2)
            self.assertGreaterEqual(differential["parser_line_difference"], 2)
            self.assertEqual(differential["afl_instrumented_objects"],
                             [Path(source_file).with_suffix(".o").name])
            self.assertEqual(differential["allowlist_entries"],
                             (project / "afl-allowlist.txt").read_text().split())
            self.assertEqual(list(differential["first_parser_lines_by_file"]), [source_file])


if __name__ == "__main__":
    unittest.main()
