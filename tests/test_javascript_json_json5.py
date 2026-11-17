"""json5 is recorded as a JSON5-superset text-API path, checked against an independent JSON tree oracle."""

import json
from pathlib import Path
import struct
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/javascript/json"
PROJECT = ROOT / "projects/json/javascript/json5"
NAME = "json5"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class Members(list):
    pass


def members(pairs: list) -> Members:
    keys = [key for key, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate key in control")
    return Members(pairs)


def oracle(data: bytes) -> object:
    """Control bytes parsed with Python's json module, not json5; objects keep member order."""
    return json.loads(data.decode("utf-8"), object_pairs_hook=members, parse_int=float, parse_float=float)


def tagged(value: object) -> dict:
    if value is None:
        return {"type": "null"}
    if isinstance(value, bool):
        return {"type": "boolean", "value": value}
    if isinstance(value, str):
        return {"type": "string", "value": value}
    if isinstance(value, float):
        return {"type": "number", "float64": struct.pack(">d", value).hex()}
    if isinstance(value, Members):
        return {"type": "object", "members": [[key, tagged(child)] for key, child in value]}
    return {"type": "array", "items": [tagged(child) for child in value]}


def summary(root: object) -> dict:
    result = {"objects": 0, "arrays": 0, "booleans": 0, "nulls": 0}
    strings, numbers, depth = [], [], 0

    def walk(value: object, level: int) -> None:
        nonlocal depth
        if isinstance(value, Members):
            result["objects"] += 1
            depth = max(depth, level + 1)
            for _, child in value:
                walk(child, level + 1)
        elif isinstance(value, list):
            result["arrays"] += 1
            depth = max(depth, level + 1)
            for child in value:
                walk(child, level + 1)
        elif value is None:
            result["nulls"] += 1
        elif isinstance(value, bool):
            result["booleans"] += 1
        elif isinstance(value, str):
            strings.append(value)
        else:
            numbers.append(value)

    walk(root, 0)
    result.update(strings=sorted(strings), numbers=sorted(numbers), max_depth=depth)
    if isinstance(root, Members):
        result.update(root="object", top_level_keys=sorted(key for key, _ in root))
    elif isinstance(root, list):
        result.update(root="array", top_level_items=len(root))
    else:
        result["root"] = "scalar"
    return dict(sorted(result.items()))


class JavaScriptJsonJson5Test(unittest.TestCase):
    def test_trees_and_summaries_match_independent_oracle(self):
        manifest = read(PROJECT / "manifest.json")
        trees = read(PROJECT / "expected-trees.json")
        report = read(BASE / "json5-tree-verification.json")
        receipt = read(PROJECT / "verification.json")
        self.assertTrue(receipt["pass"] and report["pass"])
        self.assertEqual(report["base_image_id"], receipt["image_id"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        controls = ((manifest["control"], manifest["control_sha256"], manifest["expected_output"]),
                    (manifest["differential_control"], manifest["differential_control_sha256"],
                     manifest["differential_expected_output"]))
        self.assertEqual([(item["control"], item["control_sha256"]) for item in report["results"]],
                         [(control, digest) for control, digest, _ in controls])
        for (control, digest, expected), result in zip(controls, report["results"]):
            value = oracle((ROOT / control).read_bytes())
            self.assertEqual(trees[digest]["tree"], tagged(value), control)
            self.assertEqual(summary(value), expected, control)
            self.assertTrue(result["tree_matches_oracle"] and result["summary_matches_pinned"])
            self.assertEqual(result["summary"], expected)

    def test_record_pins_release_ranks_first_and_notes_config_use(self):
        parsers = read(BASE / "parsers.json")
        parser = parsers[0]
        self.assertEqual(parser["name"], NAME)
        lock = read(PROJECT / "source-lock.json")[NAME]
        npm_lock = read(PROJECT / "package-lock.json")["packages"]
        self.assertEqual([key for key in npm_lock if key.endswith("node_modules/json5")], ["node_modules/json5"])
        self.assertEqual((lock["release"], lock["npm_integrity"], lock["source_sha256"]),
                         (parser["version"], parser["npm_integrity"], parser["tarball_sha256"]))
        self.assertEqual((npm_lock["node_modules/json5"]["version"], npm_lock["node_modules/json5"]["integrity"],
                          npm_lock["node_modules/json5"]["license"]),
                         (parser["version"], parser["npm_integrity"], parser["license"]))
        dockerfile = (PROJECT / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn(parser["tarball_sha256"], dockerfile)
        self.assertIn(read(PROJECT / "manifest.json")["base_image"], dockerfile)
        snapshot = read(BASE / "registry-snapshot.json")
        self.assertEqual(snapshot["downloads"][NAME]["value"], parser["popularity"]["value"])
        inspection = snapshot["latest_release_inspection"][NAME]
        self.assertEqual(inspection["integrity"], parser["npm_integrity"])
        self.assertEqual(inspection["json_parse_call_files"], [])
        self.assertIn("configuration-file use", parser["popularity"]["usage_note"])
        self.assertIn("not strict JSON parsing", parser["popularity"]["usage_note"])
        self.assertIn("superset", parser["scope"])
        recheck = parser["adoption_recheck"]
        self.assertEqual(recheck["npm_downloads_30d_unchanged"], parser["popularity"]["value"])
        # The weekly recheck captured the selection when json5 was added.
        self.assertTrue(set(recheck["npm_last_week"]["values"]).issubset(
            {item["name"] for item in parsers}))
        self.assertEqual(recheck["selected_count_with_this_path"],
                         len(recheck["npm_last_week"]["values"]))
        self.assertLessEqual(recheck["selected_count_with_this_path"], recheck["ceiling"])
        lead, = [lead for lead in read(BASE / "leads.json") if lead["name"] == NAME]
        self.assertEqual(lead["status"], "promoted_to_verified")
        self.assertNotIn("shared_family_with", parser)

    def test_adapter_calls_json5_parse_once_without_fallback(self):
        adapter = (PROJECT / "adapter.mjs").read_text(encoding="utf-8")
        self.assertIn("import JSON5 from 'json5';", adapter)
        self.assertIn("new TextDecoder('utf-8', { fatal: true, ignoreBOM: true })", adapter)
        self.assertIn("tree(JSON5.parse(decoder.decode(bytes)))", adapter)
        code = "\n".join(line for line in adapter.splitlines() if not line.lstrip().startswith("//"))
        self.assertEqual(code.count("JSON5.parse("), 1)
        for forbidden in ("JSON.parse", "eval(", "Function("):
            self.assertNotIn(forbidden, code)

    def test_coverage_and_feedback_stay_in_json5_parse_source(self):
        manifest = read(PROJECT / "manifest.json")
        self.assertEqual(manifest["coverage_subject_prefix"], "/work/node_modules/json5/")
        receipt = read(PROJECT / "verification.json")
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertLessEqual(receipt["format_specific_source_lines_covered"], receipt["parser_source_lines_covered"])
        result, = [item for item in read(BASE / "afl-feedback.json")["results"]
                   if item["project"] == "json/javascript/json5"]
        overlay = read(ROOT / "fuzzing/afl-native/json/javascript/json5/verification.json")
        self.assertIn("ENV PARSARIUM_SUBJECT_PREFIX=/work/node_modules/json5/\n",
                      (ROOT / "fuzzing/afl-native/json/javascript/json5/Dockerfile").read_text(encoding="utf-8"))
        self.assertEqual(result["overlay_image_id"], overlay["image_id"])
        self.assertEqual(result["base_image_id"], receipt["image_id"])
        self.assertTrue(result["repeated_control_identical"] and result["repeated_differential_identical"])
        changed = {**result["control_only_features_by_file"], **result["differential_only_features_by_file"]}
        self.assertEqual(set(changed), {"lib/parse.js"})
        self.assertGreater(result["parser_feature_difference"], 0)
        self.assertGreater(result["afl_tuple_difference"], 0)


if __name__ == "__main__":
    unittest.main()
