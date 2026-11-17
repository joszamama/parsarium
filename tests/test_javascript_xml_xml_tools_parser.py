"""Check the raw XML CST receipt against an independent raw-name Expat oracle."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/xml/javascript/xml_tools_parser"
MANIFEST = json.loads((PROJECT / "manifest.json").read_text())
spec = importlib.util.spec_from_file_location("xml_tools_oracle", PROJECT / "oracle.py")
oracle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(oracle)


class XmlToolsParserEvidenceTest(unittest.TestCase):
    def test_both_raw_name_trees_match_expat(self):
        for path_key, digest_key, output_key in (
            ("control", "control_sha256", "expected_output"),
            ("differential_control", "differential_control_sha256",
             "differential_expected_output"),
        ):
            path = ROOT / MANIFEST[path_key]
            expected = MANIFEST[output_key]
            self.assertEqual(sha256(path.read_bytes()).hexdigest(), MANIFEST[digest_key])

            def raw_names(node):
                return {"qname": node["qname"],
                        "attributes": [attribute["qname"]
                                       for attribute in node["attributes"]],
                        "children": [raw_names(child) for child in node["children"]]}

            self.assertEqual({"tree": raw_names(expected["tree"]),
                              "max_depth": expected["max_depth"]},
                             oracle.structure(path.read_bytes()))
            self.assertEqual((expected["lex_errors"], expected["parse_errors"]), (0, 0))

    def test_raw_cst_scope_and_count_feedback_receipt(self):
        first = MANIFEST["expected_output"]
        second = MANIFEST["differential_expected_output"]
        self.assertEqual(first["tree"]["qname"], "c:catalog")
        self.assertEqual(second["tree"]["children"][0]["children"][1]["qname"],
                         "p:amount")
        self.assertEqual(second["tree"]["children"][1]["attributes"][1]["raw_value"],
                         '"say &quot;hi&quot;"')
        self.assertEqual(MANIFEST["afl_js_count_functions"], ["ALT"])
        self.assertEqual(MANIFEST["afl_coverage_subject_prefix"],
                         "/work/node_modules/@xml-tools/parser/lib/parser.js")
        feedback = json.loads((ROOT / "data/javascript/xml/xml-tools-parser-feedback.json").read_text())
        self.assertTrue(feedback["read_only_baseline_identical_for_both_controls"])
        self.assertEqual(feedback["read_only_baseline_grammar_features"], 17)
        self.assertEqual(feedback["input_dependent_hit_count_ranges"], 11)
        self.assertGreater(feedback["afl_tuple_difference"], 0)


if __name__ == "__main__":
    unittest.main()
