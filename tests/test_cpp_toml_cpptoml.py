"""The C++ cpptoml TOML path keeps its pins, typed-tree oracle, metric and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/cpp/toml"
PACKAGE = "cpptoml"
RELEASE = "0.1.1"
RANK = 3
METRIC_VALUE = 5
PROJECT = ROOT / "projects/toml/cpp" / PACKAGE
OVERLAY = ROOT / "fuzzing/afl-native/toml/cpp" / PACKAGE


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class CppTomlCpptomlPilotTest(unittest.TestCase):
    def test_pins_agree(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual((manifest["release"], lock["release"]), (RELEASE, RELEASE))
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        for pinned in (lock["source_sha256"], lock["source_url"], lock["license_sha256"],
                       manifest["base_image"]):
            self.assertIn(pinned, dockerfile)
        for name in ("harness.cpp", "parser-probe.cpp"):
            self.assertIn('cpptoml::parser(stream).parse()', (PROJECT / name).read_text())
        allowlist = (PROJECT / "afl-allowlist.txt").read_text().split()
        self.assertIn('fun:_ZN7cpptoml6parser*', allowlist)

    def test_expected_trees_are_the_committed_controls(self):
        manifest = read(PROJECT / "manifest.json")
        for control, digest, expected in (
                (manifest["control"], manifest["control_sha256"], manifest["expected_output"]),
                (manifest["differential_control"], manifest["differential_control_sha256"],
                 manifest["differential_expected_output"])):
            self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)
            self.assertEqual(read(ROOT / control.replace(".toml", ".expected.json")), expected, control)
        self.assertEqual(manifest["control"], "controls/toml/service-config.toml")
        self.assertEqual(manifest["differential_control"], "controls/toml/typed-scalars.toml")

    def test_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == PACKAGE]
        record, = [item for item in read(BASE / "verification.json")["third_party"]
                   if item["package"] == PACKAGE]
        self.assertTrue(receipt["pass"] and record["pass"] and record["differential_pass"])
        self.assertTrue(receipt["fuzz_engine_smoke_pass"])
        self.assertEqual(receipt["manifest"], f"projects/toml/cpp/{PACKAGE}/manifest.json")
        self.assertEqual(receipt["source_sha256"], manifest["source_sha256"])
        self.assertEqual(receipt["control_sha256"], manifest["control_sha256"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        self.assertEqual(record["output"], manifest["expected_output"])
        self.assertEqual(record["second_valid_output"], manifest["differential_expected_output"])
        self.assertEqual(record["version"], parser["version"])
        current = {str(path.relative_to(PROJECT)): sha256(path.read_bytes()).hexdigest()
                   for path in sorted(PROJECT.rglob("*"))
                   if path.is_file() and path.name not in {"verification.json", "README.md"}
                   and "target" not in path.relative_to(PROJECT).parts}
        self.assertEqual(receipt["project_file_sha256"], current)
        self.assertGreater(receipt["parser_source_lines_covered"], 0)
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertEqual(record["parser_source_lines_covered"], receipt["parser_source_lines_covered"])
        self.assertTrue(manifest["coverage_subject_prefix"].startswith("/work/source/include/"))

    def test_metric_matches_snapshot_and_rank(self):
        parsers = read(BASE / "parsers.json")
        parser, = [item for item in parsers if item["name"] == PACKAGE]
        metric = parser["metric"]
        self.assertEqual(metric["value"], METRIC_VALUE)
        snapshot = read(BASE / "registry-snapshot.json")
        sources = {row["name"]: row["inst"] for row in snapshot["search"][0]["hits"]}
        binaries = {row["name"]: row["inst"] for row in snapshot["search"][1]["hits"]}
        self.assertEqual(sources[metric["source_package"]], METRIC_VALUE)
        self.assertEqual(binaries[metric["binary_package"]], METRIC_VALUE)
        for package, installs in metric["dev_package_installs"].items():
            self.assertEqual(binaries[package], installs)
        ranked = [item["metric"]["value"] for item in parsers]
        self.assertEqual(ranked, sorted(ranked, reverse=True))
        self.assertEqual([item["name"] for item in parsers].index(PACKAGE) + 1, RANK)
        ranking = (BASE / "ranking.md").read_text(encoding="utf-8")
        self.assertIn("| Rank | Package | Release | Metric | Parsed scope | Parser family |", ranking)
        self.assertIn(f"| {RANK} | [cpptoml]", ranking)

    def test_family_is_independent_and_lead_resolved(self):
        parsers = read(BASE / "parsers.json")
        parser, = [item for item in parsers if item["name"] == PACKAGE]
        self.assertEqual(parser["family"], 'cpptoml (skystrife)')
        self.assertEqual([item["family"] for item in parsers].count(parser["family"]), 1)
        leads = read(BASE / "leads.json")
        self.assertNotIn('cpptoml', [item["name"] for item in leads["leads"]])
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(cell["unresolved_documentation_leads"], len(leads["leads"]))

    def test_feedback_is_stable_and_differential(self):
        report = read(BASE / "afl-feedback.json")
        result, = [item for item in report["results"] if item["project"] == f"toml/cpp/{PACKAGE}"]
        differential = read(OVERLAY / "differential.json")
        overlay = read(OVERLAY / "verification.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(differential["base_project_receipt_sha256"], overlay["base_project_receipt_sha256"])
        self.assertEqual(sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
                         differential["overlay_receipt_sha256"])
        self.assertEqual(sha256((OVERLAY / "differential.json").read_bytes()).hexdigest(),
                         result["differential_receipt_sha256"])
        self.assertEqual(differential["allowlist_sha256"],
                         sha256((PROJECT / "afl-allowlist.txt").read_bytes()).hexdigest())
        self.assertTrue(differential["pass"] and differential["repeated_feedback_identical"])
        self.assertGreaterEqual(differential["repeats_per_control"], 3)
        self.assertEqual(differential["second_case_kind"], "valid_control")
        self.assertEqual(differential["first_afl_tuples"], overlay["feedback_edges"])
        self.assertGreaterEqual(differential["afl_tuple_difference"], 2)
        self.assertGreaterEqual(differential["source_line_difference"], 2)
        self.assertEqual(differential["first_source_lines"],
                         sum(differential["first_source_lines_by_file"].values()))
        self.assertEqual(result["afl_tuple_difference"], differential["afl_tuple_difference"])


if __name__ == "__main__":
    unittest.main()
