"""The Go go-rotini/toml path keeps its pins, typed trees, catalog record and AFL++ feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/go/toml"
PACKAGE = "github.com/go-rotini/toml"
RELEASE = "v1.2.2"
SLUG = "github_com_go_rotini_toml"
PROJECT = ROOT / "projects/toml/go" / SLUG
OVERLAY = ROOT / "fuzzing/afl-native/toml/go" / SLUG
METRIC = 2


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


class GoTomlGoRotiniTest(unittest.TestCase):
    def test_pins_agree(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        go_sum = (PROJECT / "go.sum").read_text()
        self.assertEqual((manifest["package"], manifest["release"], lock["release"]),
                         (PACKAGE, RELEASE, RELEASE))
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        for digest in (lock["source_sha256"], lock["license_sha256"], lock["parser_source_sha256"],
                       manifest["base_image"]):
            self.assertIn(digest, dockerfile)
        self.assertIn(f"{PACKAGE} {RELEASE} {lock['go_module_sum']}", go_sum)
        self.assertIn(f"{PACKAGE} {RELEASE}/go.mod {lock['go_mod_sum']}", go_sum)
        self.assertIn(f"require {PACKAGE} {RELEASE}", (PROJECT / "go.mod").read_text())
        self.assertIn("-coverpkg=github.com/go-rotini/toml ", dockerfile)
        self.assertEqual(lock["license"], "MIT")

    def test_controls_and_typed_trees(self):
        manifest = read(PROJECT / "manifest.json")
        for control, digest, expected in (
                ("control", "control_sha256", "expected_output"),
                ("differential_control", "differential_control_sha256", "differential_expected_output")):
            path = ROOT / manifest[control]
            self.assertEqual(sha256(path.read_bytes()).hexdigest(), manifest[digest])
            self.assertEqual(manifest[expected], read(path.with_suffix(".expected.json")))
        harness = (PROJECT / "harness_test.go").read_text(encoding="utf-8")
        self.assertIn(f"const expectedJSON = `{canonical(manifest['expected_output'])}`", harness)
        self.assertIn(f"const differentialJSON = `{canonical(manifest['differential_expected_output'])}`", harness)

    def test_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        record, = [item for item in read(BASE / "verification.json")["third_party"]
                   if item["package"] == PACKAGE]
        self.assertTrue(receipt["pass"] and receipt["fuzz_engine_smoke_pass"])
        self.assertTrue(record["pass"] and record["differential_control_pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        self.assertEqual(record["output"], manifest["expected_output"])
        self.assertEqual(record["differential_output"], manifest["differential_expected_output"])
        self.assertEqual(receipt["source_sha256"], manifest["source_sha256"])
        self.assertEqual(receipt["control_sha256"], manifest["control_sha256"])
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        self.assertGreater(receipt["parser_source_lines_covered"], 0)
        self.assertEqual(record["parser_source_lines_covered"], receipt["parser_source_lines_covered"])
        self.assertEqual((parser["version"], parser["metric"]["value"]), (RELEASE, METRIC))
        snapshot = read(BASE / "registry-snapshot.json")
        self.assertIn(METRIC, {hit["imported_by"] for query in snapshot["search"]
                               for hit in query["hits"] if hit["name"] == PACKAGE})

    def test_cell_and_leads(self):
        cell = read(BASE / "cell.json")
        parsers = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")["leads"]
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(cell["unresolved_documentation_leads"], len(leads))
        self.assertNotIn(PACKAGE, {lead["name"] for lead in leads})
        self.assertIn(f"[{PACKAGE}](", (BASE / "ranking.md").read_text())
        self.assertTrue((BASE / "ranking.md").read_text().count(
            "| Rank | Package | Release | Metric | Parsed scope | Parser family |") == 1)

    def test_feedback_is_stable_and_differential(self):
        result, = [item for item in read(BASE / "afl-feedback.json")["results"]
                   if item["project"] == f"toml/go/{SLUG}"]
        overlay = read(OVERLAY / "verification.json")
        receipt = read(PROJECT / "verification.json")
        self.assertEqual(sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
                         result["overlay_receipt_sha256"])
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertTrue(result["pass"] and result["repeated_control_identical"]
                        and result["repeated_differential_identical"])
        self.assertGreaterEqual(result["repeats_per_control"], 3)
        self.assertGreaterEqual(result["afl_tuple_difference"], 2)
        self.assertGreaterEqual(result["parser_feature_difference"], 2)
        self.assertEqual(result["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(result["control_afl_tuples"], overlay["feedback_edges"])
        self.assertEqual(result["control_parser_source_lines"], receipt["parser_source_lines_covered"])
        self.assertEqual(sum(result["control_parser_lines_per_file"].values()),
                         result["control_parser_source_lines"])
        self.assertIn("parser.go", result["differential_parser_lines_per_file"])
        self.assertIn("scanner.go", result["differential_parser_lines_per_file"])
        self.assertIn("ENV PARSARIUM_SUBJECT_PREFIX=github.com/go-rotini/toml/",
                      (OVERLAY / "Dockerfile").read_text())


if __name__ == "__main__":
    unittest.main()
