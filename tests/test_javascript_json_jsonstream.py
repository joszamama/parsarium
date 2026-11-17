"""JSONStream is recorded as a separate API path over the shared jsonparse family."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/javascript/json"
PROJECT = ROOT / "projects/json/javascript/jsonstream"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class JavaScriptJsonJsonStreamTest(unittest.TestCase):
    def test_record_names_shared_family_and_pinned_dependencies(self):
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "JSONStream"]
        self.assertEqual(parser["shared_family_with"], "jsonparse")
        self.assertIs(parser["independent_engine"], False)
        lock = read(PROJECT / "source-lock.json")["JSONStream"]
        npm_lock = read(PROJECT / "package-lock.json")["packages"]
        self.assertEqual(lock["npm_integrity"], parser["npm_integrity"])
        self.assertEqual(lock["source_sha256"], parser["tarball_sha256"])
        self.assertEqual(npm_lock["node_modules/JSONStream"]["integrity"], parser["npm_integrity"])
        for dependency in parser["dependencies"]:
            pinned = lock["dependencies"][dependency["name"]]
            self.assertEqual(pinned["release"], dependency["version"])
            self.assertEqual(pinned["npm_integrity"], dependency["npm_integrity"])
            self.assertEqual(pinned["source_sha256"], dependency["tarball_sha256"])
            locked = npm_lock[f"node_modules/{dependency['name']}"]
            self.assertEqual((locked["version"], locked["integrity"]),
                             (dependency["version"], dependency["npm_integrity"]))
        self.assertEqual(set(npm_lock["node_modules/JSONStream"]["dependencies"]),
                         {dependency["name"] for dependency in parser["dependencies"]})
        snapshot = read(BASE / "registry-snapshot.json")
        self.assertEqual(snapshot["downloads"]["JSONStream"]["value"], parser["popularity"]["value"])
        self.assertEqual(snapshot["latest_release_inspection"]["JSONStream"]["integrity"], parser["npm_integrity"])
        lead, = [lead for lead in read(BASE / "leads.json") if lead["name"] == "JSONStream"]
        self.assertEqual(lead["status"], "promoted_to_verified")

    def test_adapter_uses_stream_api_and_requires_one_root(self):
        adapter = (PROJECT / "adapter.mjs").read_text(encoding="utf-8")
        self.assertIn("JSONStream.parse([])", adapter)
        self.assertIn("stream.end(bytes)", adapter)
        self.assertIn("!ended || roots.length !== 1", adapter)
        self.assertNotIn("JSON.parse", adapter)
        self.assertNotIn("jsonparse", adapter.split("import JSONStream", 1)[1].split("\n", 1)[0])

    def test_coverage_separates_package_and_underlying_source(self):
        manifest = read(PROJECT / "manifest.json")
        self.assertEqual(manifest["coverage_subject_prefix"], "/work/node_modules/JSONStream/")
        self.assertEqual(manifest["underlying_coverage_subject_prefix"], "/work/node_modules/jsonparse/")
        receipt = read(PROJECT / "verification.json")
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        self.assertEqual((receipt["parser_source_files"], receipt["underlying_source_files"]), (1, 1))
        self.assertGreater(receipt["parser_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)

    def test_feedback_differs_only_where_recorded(self):
        manifest = read(PROJECT / "manifest.json")
        feedback = read(BASE / "jsonstream-afl-feedback.json")
        self.assertEqual(feedback["control_output"], manifest["expected_output"])
        self.assertEqual(feedback["differential_output"], manifest["differential_expected_output"])
        self.assertTrue(feedback["repeated_control_identical"] and feedback["repeated_differential_identical"])
        self.assertGreater(feedback["parser_feature_difference"], 0)
        self.assertGreater(feedback["afl_tuple_difference"], 0)
        changed = feedback["feature_difference_by_package"]
        self.assertEqual(sum(changed.values()), feedback["parser_feature_difference"])
        self.assertGreater(changed["jsonparse"], 0)
        self.assertEqual(feedback["package_only_feedback_differs"], changed["JSONStream"] > 0)
        overlay = read(ROOT / "fuzzing/afl-native/json/javascript/jsonstream/verification.json")
        self.assertEqual(feedback["overlay_image_id"], overlay["image_id"])


if __name__ == "__main__":
    unittest.main()
