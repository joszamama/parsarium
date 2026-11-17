"""The Python YAML ruamel.yaml pure safe-loader path keeps its catalog, lock, oracle, receipts and feedback consistent."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SLUG = "ruamel_yaml"
NAME = "ruamel.yaml"
BASE = ROOT / "data/python/yaml"
PROJECT = ROOT / "projects/yaml/python" / SLUG
OVERLAY = ROOT / "fuzzing/afl-native/yaml/python" / SLUG
_spec = importlib.util.spec_from_file_location("yaml_check_controls", ROOT / "controls/yaml/check_controls.py")
ORACLE = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ORACLE)


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class PythonYamlPilotTest(unittest.TestCase):
    def parser(self) -> dict:
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == NAME]
        return parser

    def test_metric_and_lead_match_the_snapshot(self):
        parsers = read(BASE / "parsers.json")
        snapshot = read(BASE / "registry-snapshot.json")
        metrics = [item["popularity"]["value"] for item in parsers]
        self.assertEqual(metrics, sorted(metrics, reverse=True))
        self.assertEqual(self.parser()["popularity"]["value"], snapshot["metrics"][NAME]["value"])
        lead, = [item for item in read(BASE / "leads.json") if item["name"] == NAME]
        self.assertEqual(lead["status"], "selected")
        self.assertEqual(lead["metric_value"], self.parser()["popularity"]["value"])
        self.assertEqual(len(parsers), read(BASE / "cell.json")["verified_third_party_count"])

    def test_release_lock_matches_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        parser = self.parser()
        dockerfile = (PROJECT / "Dockerfile").read_text()
        lock = (PROJECT / "runtime-requirements.lock").read_text().splitlines()
        self.assertEqual(parser["wheel_sha256"], manifest["source_sha256"])
        self.assertEqual(parser["source_sha256"], manifest["sdist_sha256"])
        self.assertEqual(lock[0], f"{NAME}=={manifest['release']} --hash=sha256:{manifest['source_sha256']}")
        for digest in (manifest["source_sha256"], manifest["sdist_sha256"], manifest["fuzz_engine_sha256"]):
            self.assertIn(digest, dockerfile)
        self.assertIn("grep -Fx 'License: MIT'", dockerfile)
        self.assertIn("YAML(typ='safe', pure=True)", (PROJECT / "harness.py").read_text())
        self.assertIn("loader.Parser is ruamel.yaml.parser.Parser", (PROJECT / "harness.py").read_text())

    def test_expected_outputs_are_the_hand_written_trees(self):
        manifest = read(PROJECT / "manifest.json")
        parser = self.parser()
        for key, control in (("expected_output", "catalog.yaml"), ("differential_expected_output", "order.yaml")):
            self.assertEqual(manifest[key]["tree"], ORACLE.EXPECTED[control])
            self.assertEqual(manifest[key]["tree_sha256"], ORACLE.tree_sha256(ORACLE.EXPECTED[control]))
            self.assertEqual(parser[key], manifest[key])
        self.assertEqual(read(PROJECT / "expected.json"), manifest["expected_output"])

    def test_project_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], self.parser()["expected_output"])
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        for control, digest in ((manifest["control"], manifest["control_sha256"]),
                                (manifest["differential_control"], manifest["differential_control_sha256"])):
            self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        record, = [item for item in read(BASE / "verification.json")["third_party"] if item["package"] == NAME]
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(record["parser_source_lines_covered"], receipt["parser_source_lines_covered"])

    def test_feedback_is_exact_stable_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / f"{SLUG}-valid-feedback.json")
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
        self.assertGreater(report["scanner_py_feature_difference"] + report["parser_py_feature_difference"], 0)
        self.assertGreater(report["afl_tuple_difference"], 0)
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(report["control_afl_tuples"], overlay["feedback_edges"])


if __name__ == "__main__":
    unittest.main()
