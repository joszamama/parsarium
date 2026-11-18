"""The Python TOML tomlclass path keeps its catalog, lock, controls, receipts and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/toml"
SLUG = "tomlclass"
RELEASE = "0.4.1"
METRIC = 2652
PARSER_FILE = "parser.py"
PROJECT = ROOT / "projects/toml/python" / SLUG
OVERLAY = ROOT / "fuzzing/afl-native/toml/python" / SLUG


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PythonTomlTomlclassPilotTest(unittest.TestCase):
    def parser(self) -> dict:
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == SLUG]
        return parser

    def test_cell_counts_and_metric(self):
        parsers = read(BASE / "parsers.json")
        cell = read(BASE / "cell.json")
        leads = read(BASE / "leads.json")["leads"]
        packages = read(BASE / "registry-snapshot.json")["adoption_metric"]["packages"]
        self.assertEqual(len(parsers), cell["verified_third_party_count"])
        self.assertEqual(cell["verified_standard_or_runtime_count"], 1)
        self.assertEqual(len(read(BASE / "standard.json")["verified_apis"]), 1)
        self.assertEqual(len(leads), cell["unresolved_documentation_leads"])
        self.assertNotIn(SLUG, {lead["name"] for lead in leads})
        values = [parser["metric"]["value"] for parser in parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        for parser in parsers:
            self.assertEqual(parser["metric"]["value"], packages[parser["name"]]["value"])
        self.assertEqual(self.parser()["metric"]["value"], METRIC)
        ranking = (BASE / "ranking.md").read_text(encoding="utf-8")
        self.assertIn("| Rank | Package | Release | PyPI downloads (last month) | Parsed scope | Parser family |", ranking)
        self.assertIn(f"[{SLUG}](", ranking)

    def test_release_lock_matches_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        parser = self.parser()
        lock = read(PROJECT / "source-lock.json")[SLUG]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        requirements = (PROJECT / "runtime-requirements.lock").read_text()
        self.assertEqual(manifest["release"], RELEASE)
        self.assertEqual(parser["version"], RELEASE)
        self.assertEqual(lock["release"], RELEASE)
        self.assertEqual(lock["wheel_sha256"], manifest["source_sha256"])
        self.assertEqual(lock["sdist_sha256"], manifest["sdist_sha256"])
        self.assertEqual(parser["wheel_sha256"], manifest["source_sha256"])
        self.assertEqual(parser["source_sha256"], manifest["sdist_sha256"])
        self.assertEqual(parser["license"], "MIT")
        self.assertEqual(lock["license"], "MIT")
        self.assertIn("License-Expression: MIT", dockerfile)
        self.assertEqual(requirements.splitlines(), [
            f"{SLUG}=={RELEASE} --hash=sha256:{manifest['source_sha256']}",
            f"atheris=={manifest['fuzz_engine_release']} --hash=sha256:{manifest['fuzz_engine_sha256']}"])
        for digest in (manifest["source_sha256"], manifest["sdist_sha256"], manifest["fuzz_engine_sha256"],
                       manifest["base_image"].split("@")[1]):
            self.assertIn(digest, dockerfile)
        for name, digest in lock["source_file_sha256"].items():
            self.assertIn(f"{digest}  {name}", dockerfile)

    def test_controls_and_expected_trees(self):
        manifest = read(PROJECT / "manifest.json")
        parser = self.parser()
        for control, digest, tree in (
                (manifest["control"], manifest["control_sha256"], manifest["expected_output"]),
                (manifest["differential_control"], manifest["differential_control_sha256"],
                 manifest["differential_expected_output"])):
            path = ROOT / control
            self.assertEqual(sha256(path.read_bytes()).hexdigest(), digest)
            committed = path.with_name(path.stem + ".expected.json")
            self.assertEqual(read(committed), tree)
            self.assertEqual((PROJECT / "expected" / committed.name).read_bytes(), committed.read_bytes())
        self.assertEqual(manifest["control"], "controls/toml/service-config.toml")
        self.assertEqual(manifest["differential_control"], "controls/toml/typed-scalars.toml")
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        self.assertEqual(parser["differential_expected_output"], manifest["differential_expected_output"])
        self.assertEqual(manifest["format"], "toml")
        self.assertTrue(manifest["coverage_subject_prefix"].endswith(f"/site-packages/{SLUG}/"))

    def test_project_receipt_matches_catalog(self):
        receipt = read(PROJECT / "verification.json")
        parser = self.parser()
        self.assertTrue(receipt["pass"] and receipt["fuzz_engine_smoke_pass"])
        self.assertEqual(receipt["output"], parser["expected_output"])
        self.assertGreater(receipt["parser_source_lines_covered"], 0)
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        record, = [item for item in read(BASE / "verification.json")["third_party"] if item["package"] == SLUG]
        self.assertTrue(record["pass"])
        self.assertEqual(record["version"], RELEASE)
        self.assertEqual(record["output"], receipt["output"])
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(record["parser_source_lines_covered"], receipt["parser_source_lines_covered"])

    def test_feedback_is_stable_scoped_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / f"{SLUG}-valid-feedback.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(overlay["control_sha256"], manifest["control_sha256"])
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertTrue(report["pass"] and report["control_repeat_identical"] and report["variant_repeat_identical"])
        self.assertGreaterEqual(report["runs_per_control"], 3)
        self.assertEqual(report["format_parser_file"], PARSER_FILE)
        self.assertGreaterEqual(report["afl_tuple_difference"], 2)
        self.assertGreaterEqual(report["parser_feature_difference"], 2)
        self.assertGreater(report["format_parser_feature_difference"], 0)
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(report["control_afl_tuples"], overlay["feedback_edges"])
        self.assertEqual(sum(report["control_parser_lines_per_file"].values()), report["control_parser_features"])
        self.assertEqual(sum(report["variant_parser_lines_per_file"].values()), report["variant_parser_features"])
        for oracle in (report["control_oracle"], report["variant_oracle"]):
            self.assertEqual(oracle["package_version"], RELEASE)
            self.assertTrue(oracle["stdlib_tomllib_matches"])
        self.assertNotEqual(report["control_oracle"]["tree_sha256"], report["variant_oracle"]["tree_sha256"])


if __name__ == "__main__":
    unittest.main()
