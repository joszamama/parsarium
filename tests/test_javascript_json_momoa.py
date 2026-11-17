"""momoa is recorded as its own text-API parser path, checked against an independent JSON summary."""

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/javascript/json"
PROJECT = ROOT / "projects/json/javascript/humanwhocodes_momoa"
NAME = "@humanwhocodes/momoa"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def no_duplicates(pairs: list) -> dict:
    keys = [key for key, _ in pairs]
    if len(keys) != len(set(keys)):
        raise ValueError("duplicate key in control")
    return dict(pairs)


def oracle(data: bytes) -> dict:
    """Summary of the control computed with Python's json module, not momoa."""
    root = json.loads(data.decode("utf-8"), object_pairs_hook=no_duplicates)
    result = {"objects": 0, "arrays": 0, "booleans": 0, "nulls": 0}
    strings, numbers, depth = [], [], 0

    def walk(value: object, level: int) -> None:
        nonlocal depth
        if isinstance(value, list):
            result["arrays"] += 1
            depth = max(depth, level + 1)
            for child in value:
                walk(child, level + 1)
        elif isinstance(value, dict):
            result["objects"] += 1
            depth = max(depth, level + 1)
            for child in value.values():
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
    if isinstance(root, list):
        result.update(root="array", top_level_items=len(root))
    elif isinstance(root, dict):
        result.update(root="object", top_level_keys=sorted(root))
    else:
        result["root"] = "scalar"
    return dict(sorted(result.items()))


class JavaScriptJsonMomoaTest(unittest.TestCase):
    def test_pinned_outputs_match_independent_oracle(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        for control, expected in ((manifest["control"], manifest["expected_output"]),
                                  (manifest["differential_control"], manifest["differential_expected_output"])):
            self.assertEqual(oracle((ROOT / control).read_bytes()), expected, control)

    def test_record_pins_release_and_ranks_by_snapshot(self):
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == NAME]
        lock = read(PROJECT / "source-lock.json")[NAME]
        npm_lock = read(PROJECT / "package-lock.json")["packages"][f"node_modules/{NAME}"]
        self.assertEqual((lock["release"], lock["npm_integrity"], lock["source_sha256"]),
                         (parser["version"], parser["npm_integrity"], parser["tarball_sha256"]))
        self.assertEqual((npm_lock["version"], npm_lock["integrity"]), (parser["version"], parser["npm_integrity"]))
        self.assertIn(parser["tarball_sha256"], (PROJECT / "Dockerfile").read_text(encoding="utf-8"))
        snapshot = read(BASE / "registry-snapshot.json")
        self.assertEqual(snapshot["downloads"][NAME]["value"], parser["popularity"]["value"])
        inspection = snapshot["latest_release_inspection"][NAME]
        self.assertEqual(inspection["integrity"], parser["npm_integrity"])
        self.assertEqual(inspection["json_parse_call_files"], [])
        recheck = parser["adoption_recheck"]
        self.assertEqual(recheck["npm_downloads_30d_unchanged"], parser["popularity"]["value"])
        weekly = recheck["npm_last_week"]["values"]
        # The recheck lists the paths selected when momoa was added.
        self.assertTrue(set(weekly).issubset({item["name"] for item in read(BASE / "parsers.json")}))
        self.assertLessEqual(recheck["selected_count_with_this_path"], recheck["ceiling"])
        self.assertEqual(recheck["selected_count_with_this_path"], len(weekly))
        lead, = [lead for lead in read(BASE / "leads.json") if lead["name"] == NAME]
        self.assertEqual(lead["status"], "promoted_to_verified")
        self.assertNotIn("shared_family_with", parser)

    def test_adapter_uses_documented_text_api_and_ast(self):
        adapter = (PROJECT / "adapter.mjs").read_text(encoding="utf-8")
        self.assertIn("import { parse as parseJson } from '@humanwhocodes/momoa';", adapter)
        self.assertIn("new TextDecoder('utf-8', { fatal: true, ignoreBOM: true })", adapter)
        self.assertIn("parseJson(decoder.decode(bytes), { mode: 'json' })", adapter)
        code = "\n".join(line for line in adapter.splitlines() if not line.lstrip().startswith("//"))
        for forbidden in ("JSON.parse", "evaluate"):
            self.assertNotIn(forbidden, code)

    def test_coverage_and_feedback_stay_in_momoa_source(self):
        manifest = read(PROJECT / "manifest.json")
        prefix = "/work/node_modules/@humanwhocodes/momoa/"
        self.assertEqual(manifest["coverage_subject_prefix"], prefix)
        receipt = read(PROJECT / "verification.json")
        self.assertEqual(receipt["parser_source_files"], 1)
        self.assertGreater(receipt["parser_source_lines_covered"], 0)
        result, = [item for item in read(BASE / "afl-feedback.json")["results"]
                   if item["project"] == "json/javascript/humanwhocodes_momoa"]
        overlay = read(ROOT / "fuzzing/afl-native/json/javascript/humanwhocodes_momoa/verification.json")
        self.assertEqual(result["overlay_image_id"], overlay["image_id"])
        self.assertEqual(result["base_image_id"], receipt["image_id"])
        self.assertTrue(result["repeated_control_identical"] and result["repeated_differential_identical"])
        changed = {**result["control_only_features_by_file"], **result["differential_only_features_by_file"]}
        self.assertEqual(set(changed), {"dist/momoa.js"})
        self.assertGreater(result["parser_feature_difference"], 0)
        self.assertGreater(result["afl_tuple_difference"], 0)


if __name__ == "__main__":
    unittest.main()
