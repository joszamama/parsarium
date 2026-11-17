"""The Python JSON msgspec path keeps its catalog, lock, receipts, and feedback consistent."""

from hashlib import sha256
import json
import math
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/json"
PROJECT = ROOT / "projects/json/python/msgspec"
OVERLAY = ROOT / "fuzzing/afl-native/json/python/msgspec"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def untag(node: list) -> object:
    """Rebuild plain Python values from a hand-written type-tagged tree."""
    kind, *rest = node
    if kind == "object":
        return {key: untag(item) for key, item in rest[0]}
    if kind == "array":
        return [untag(item) for item in rest[0]]
    if kind == "float":
        return float(rest[0])
    return None if kind == "null" else rest[0]


def same_types(left: object, right: object) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, dict):
        return list(left) == list(right) and all(same_types(left[k], right[k]) for k in left)
    if isinstance(left, list):
        return len(left) == len(right) and all(map(same_types, left, right))
    return left == right or (isinstance(left, float) and math.isclose(left, right))


class PythonJsonMsgspecPilotTest(unittest.TestCase):
    def test_hand_written_trees_agree_with_cpython_json(self):
        manifest = read(PROJECT / "manifest.json")
        for control, expected in ((manifest["control"], manifest["expected_output"]),
                                  (manifest["differential_control"],
                                   manifest["differential_expected_output"])):
            reference = json.loads((ROOT / control).read_bytes())
            self.assertTrue(same_types(untag(expected["value"]), reference), control)

    def test_lead_and_rank(self):
        parsers = read(BASE / "parsers.json")
        leads = {lead["name"]: lead for lead in read(BASE / "leads.json")["leads"]}
        parser, = [item for item in parsers if item["name"] == "msgspec"]
        self.assertEqual(leads["msgspec"]["status"], "promoted_to_verified")
        self.assertEqual(parser["popularity"]["value"], leads["msgspec"]["last_month"])
        self.assertLess(leads["msgspec"]["last_month"], leads["ijson"]["last_month"])
        self.assertGreater(leads["msgspec"]["last_month"], leads["ujson"]["last_month"])

    def test_release_lock_matches_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "msgspec"]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        requirements = (PROJECT / "build-requirements.lock").read_text()
        self.assertEqual(lock["msgspec"]["release"], manifest["release"])
        self.assertEqual(lock["msgspec"]["sdist_sha256"], manifest["source_sha256"])
        self.assertEqual(parser["source_sha256"], manifest["source_sha256"])
        self.assertEqual(parser["wheel_sha256"], lock["msgspec"]["wheel_sha256"])
        self.assertEqual(parser["license"], lock["msgspec"]["license"])
        self.assertEqual(lock["msgspec"]["runtime_dependencies"], [])
        for digest in (manifest["source_sha256"], lock["msgspec"]["core_c_sha256"],
                       lock["msgspec"]["atof_h_sha256"], lock["msgspec"]["license_file_sha256"],
                       lock["msgspec"]["commit"]):
            self.assertIn(digest, dockerfile)
        for name, pin in lock["build_backend"].items():
            if isinstance(pin, dict):
                self.assertIn(f"{name}=={pin['release']} --hash=sha256:{pin['wheel_sha256']}",
                              requirements)
        self.assertNotIn("MSGSPEC_DEBUG=", dockerfile)

    def test_project_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "msgspec"]
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], parser["expected_output"])
        self.assertEqual(manifest["differential_expected_output"],
                         parser["differential_expected_output"])
        for control, digest in ((manifest["control"], manifest["control_sha256"]),
                                (manifest["differential_control"],
                                 manifest["differential_control_sha256"])):
            self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        record, = [item for item in read(BASE / "verification.json")["third_party"]
                   if item["package"] == "msgspec"]
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(record["output"], receipt["output"])
        self.assertGreater(record["json_decoder_region_start_lines"], 0)

    def test_feedback_is_stable_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / "msgspec-valid-feedback.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertTrue(report["pass"] and report["control_repeat_identical"]
                        and report["variant_repeat_identical"])
        self.assertEqual(report["control_output"], manifest["expected_output"])
        self.assertEqual(report["variant_output"], manifest["differential_expected_output"])
        self.assertEqual(report["json_decoder_section_lines"],
                         manifest["json_parser_source_sections"]["json_decoder_lines"])
        self.assertGreater(report["parser_feature_difference"], 0)
        self.assertGreater(report["json_decoder_feature_difference"], 0)
        self.assertGreater(report["afl_tuple_difference"], 0)
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])


if __name__ == "__main__":
    unittest.main()
