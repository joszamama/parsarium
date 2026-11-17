"""The Python TOML pytomlpp path (pybind11 over the C++ toml++ family) keeps its catalog, lock, receipts and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/toml"
SLUG = "pytomlpp"
RELEASE = "1.1.0"
METRIC = 43243
PARSER_FILE = "impl/parser.inl"
PREFIX = "/work/pytomlpp-source/third_party/tomlplusplus/include/toml++/"
PROJECT = ROOT / "projects/toml/python" / SLUG
OVERLAY = ROOT / "fuzzing/afl-native/toml/python" / SLUG


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PythonTomlPytomlppPilotTest(unittest.TestCase):
    def parser(self) -> dict:
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == SLUG]
        return parser

    def test_cell_counts_metric_and_family(self):
        parsers = read(BASE / "parsers.json")
        cell = read(BASE / "cell.json")
        leads = read(BASE / "leads.json")
        packages = read(BASE / "registry-snapshot.json")["adoption_metric"]["packages"]
        self.assertEqual(len(parsers), cell["verified_third_party_count"])
        self.assertEqual(len(leads["leads"]), cell["unresolved_documentation_leads"])
        self.assertNotIn(SLUG, {lead["name"] for lead in leads["leads"]})
        self.assertIn(SLUG, {item["name"] for item in leads["promoted"]})
        self.assertEqual(self.parser()["metric"]["value"], METRIC)
        self.assertEqual(packages[SLUG]["value"], METRIC)
        self.assertIn("toml++", self.parser()["family"])
        self.assertIn("e7aaccca", self.parser()["family_note"])
        self.assertIn(f"[{SLUG}](", (BASE / "ranking.md").read_text(encoding="utf-8"))

    def test_source_lock_matches_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        parser = self.parser()
        lock = read(PROJECT / "source-lock.json")
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual(manifest["release"], RELEASE)
        self.assertEqual(parser["version"], RELEASE)
        self.assertEqual(lock[SLUG]["release"], RELEASE)
        self.assertEqual(lock[SLUG]["sdist_sha256"], manifest["source_sha256"])
        self.assertEqual(parser["source_sha256"], manifest["source_sha256"])
        self.assertEqual(lock[SLUG]["license"], "MIT")
        self.assertIn("License :: OSI Approved :: MIT License", dockerfile)
        self.assertIn("-fprofile-instr-generate -fcoverage-mapping", dockerfile)
        for digest in (manifest["source_sha256"], manifest["base_image"].split("@")[1]):
            self.assertIn(digest, dockerfile)
        for name, digest in lock[SLUG]["source_file_sha256"].items():
            self.assertIn(f"{digest}  {name}", dockerfile)
        requirements = (PROJECT / "build-requirements.lock").read_text().splitlines()
        for name, record in (("pybind11", lock["build_backend"]["pybind11"]),
                             ("setuptools", lock["build_backend"]["setuptools"])):
            self.assertIn(f"{name}=={record['release']} --hash=sha256:{record['wheel_sha256']}", requirements)
        self.assertEqual(lock["tomlplusplus"]["submodule_commit"], "e7aaccca3fa3dbde9818ab8313250f3da4976e37")
        self.assertEqual(manifest["coverage_subject_prefix"], PREFIX)
        self.assertNotIn("afl_coverage_subject_prefix", manifest)

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
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        self.assertEqual(parser["differential_expected_output"], manifest["differential_expected_output"])

    def test_project_receipt_matches_catalog(self):
        receipt = read(PROJECT / "verification.json")
        self.assertTrue(receipt["pass"] and receipt["fuzz_engine_smoke_pass"])
        self.assertEqual(receipt["output"], self.parser()["expected_output"])
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        record, = [item for item in read(BASE / "verification.json")["third_party"] if item["package"] == SLUG]
        self.assertTrue(record["pass"])
        self.assertEqual(record["output"], receipt["output"])
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(record["parser_source_lines_covered"], receipt["parser_source_lines_covered"])

    def test_feedback_is_stable_scoped_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / f"{SLUG}-valid-feedback.json")
        self.assertEqual(overlay["feedback_kind"], "llvm_native_parser_regions_to_afl_bitmap")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertIn(f"ENV PARSARIUM_LLVM_MODULE_GLOB={manifest['afl_llvm_module_glob']}",
                      (OVERLAY / "Dockerfile").read_text())
        self.assertTrue(report["pass"] and report["control_repeat_identical"] and report["variant_repeat_identical"])
        self.assertGreaterEqual(report["runs_per_control"], 3)
        self.assertEqual(report["format_parser_file"], PARSER_FILE)
        self.assertGreater(report["format_parser_feature_difference"], 0)
        self.assertGreaterEqual(report["afl_tuple_difference"], 2)
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(report["control_afl_tuples"], overlay["feedback_edges"])
        self.assertEqual(sum(report["control_parser_lines_per_file"].values()), report["control_parser_features"])
        for name in report["control_parser_lines_per_file"]:
            self.assertTrue(name.startswith("impl/") or name.endswith((".h", ".hpp")), name)
        for oracle in (report["control_oracle"], report["variant_oracle"]):
            self.assertEqual(oracle["package_version"], RELEASE)
            self.assertTrue(oracle["stdlib_tomllib_matches"])


if __name__ == "__main__":
    unittest.main()
