"""The Python YAML ryaml path keeps its catalog, locks, oracle, receipts and native Rust feedback consistent."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SLUG = "ryaml"
NAME = "ryaml"
BASE = ROOT / "data/python/yaml"
PROJECT = ROOT / "projects/yaml/python" / SLUG
OVERLAY = ROOT / "fuzzing/afl-native/yaml/python" / SLUG
REGISTRY = "/usr/local/cargo/registry/src/index.crates.io-1949cf8c6b5b557f/"
_spec = importlib.util.spec_from_file_location("yaml_check_controls", ROOT / "controls/yaml/check_controls.py")
ORACLE = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ORACLE)


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PythonYamlRyamlPilotTest(unittest.TestCase):
    def parser(self) -> dict:
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == NAME]
        return parser

    def test_metric_is_the_recorded_snapshot_value(self):
        parsers = read(BASE / "parsers.json")
        snapshot = read(BASE / "registry-snapshot.json")
        metrics = [item["popularity"]["value"] for item in parsers]
        self.assertEqual(metrics, sorted(metrics, reverse=True))
        self.assertEqual(self.parser()["popularity"]["value"], snapshot["metrics"][NAME]["value"])
        lead, = [item for item in read(BASE / "leads.json") if item["name"] == NAME]
        self.assertEqual(lead["status"], "selected")
        self.assertEqual(lead["metric_value"], self.parser()["popularity"]["value"])
        self.assertEqual(len(parsers), read(BASE / "cell.json")["verified_third_party_count"])

    def test_sdist_and_crates_are_pinned(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")
        dockerfile = (PROJECT / "Dockerfile").read_text()
        self.assertEqual(lock[NAME]["release"], manifest["release"])
        self.assertEqual(lock[NAME]["source_sha256"], manifest["source_sha256"])
        self.assertEqual(self.parser()["source_sha256"], manifest["source_sha256"])
        for key in ("source_sha256", "lib_rs_sha256", "cargo_lock_sha256", "license_file_sha256"):
            self.assertIn(lock[NAME][key], dockerfile)
        for crate in lock["crates"].values():
            self.assertIn(crate["checksum"], dockerfile)
        self.assertIn("MATURIN_PEP517_ARGS='--locked'", dockerfile)
        self.assertIn("-C instrument-coverage", dockerfile)
        for line in (PROJECT / "build-requirements.lock").read_text().splitlines():
            self.assertIn(line.split("sha256:")[1], json.dumps(lock["build_backend"]))
        harness = (PROJECT / "harness.py").read_text()
        self.assertIn("ryaml.loads(data.decode('utf-8'))", harness)
        self.assertIn("ryaml.load(io.BytesIO(data))", harness)

    def test_expected_outputs_are_the_hand_written_trees(self):
        manifest = read(PROJECT / "manifest.json")
        parser = self.parser()
        for key, control in (("expected_output", "catalog.yaml"), ("differential_expected_output", "order.yaml")):
            self.assertEqual(manifest[key]["tree"], ORACLE.EXPECTED[control])
            self.assertEqual(manifest[key]["tree_sha256"], ORACLE.tree_sha256(ORACLE.EXPECTED[control]))
            self.assertEqual(parser[key], manifest[key])
        self.assertEqual(read(PROJECT / "expected.json"), manifest["expected_output"])

    def test_project_receipt_counts_native_parser_lines(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], self.parser()["expected_output"])
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        self.assertEqual(manifest["coverage_subject_prefix"], REGISTRY + "unsafe-libyaml-0.2.11/src/")
        for control, digest in ((manifest["control"], manifest["control_sha256"]),
                                (manifest["differential_control"], manifest["differential_control_sha256"])):
            self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        record, = [item for item in read(BASE / "verification.json")["third_party"] if item["package"] == NAME]
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(record["parser_source_lines_covered"], receipt["parser_source_lines_covered"])

    def test_native_feedback_is_exact_stable_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / f"{SLUG}-valid-feedback.json")
        self.assertEqual(overlay["feedback_kind"], "llvm_native_parser_regions_to_afl_bitmap")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        for oracle in (report["control_oracle"], report["variant_oracle"]):
            self.assertTrue(oracle["bytes_matches_oracle"] and oracle["str_matches_oracle"]
                            and oracle["stream_matches_oracle"])
        self.assertTrue(report["pass"] and report["control_repeat_identical"] and report["variant_repeat_identical"])
        self.assertGreaterEqual(report["runs_per_control"], 3)
        self.assertEqual(report["control_output"], manifest["expected_output"])
        self.assertEqual(report["variant_output"], manifest["differential_expected_output"])
        self.assertGreater(report["scanner_rs_feature_difference"] + report["parser_rs_feature_difference"], 0)
        self.assertGreater(report["afl_tuple_difference"], 0)
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(report["control_afl_tuples"], overlay["feedback_edges"])


if __name__ == "__main__":
    unittest.main()
