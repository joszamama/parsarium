"""The standalone jiter path keeps its catalog, lock, oracle, receipts, and native Jiter feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import re
import sys
import types
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/python/json"
PROJECT = ROOT / "projects/json/python/jiter"
OVERLAY = ROOT / "fuzzing/afl-native/json/python/jiter"
JITER_SRC = "/work/jiter-source/crates/jiter/src/"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def harness_summarize():
    """Load the harness summarizer with CPython json standing in for jiter."""
    saved = sys.modules.get("jiter")
    sys.modules["jiter"] = types.SimpleNamespace(from_json=json.loads)
    try:
        namespace = {"__name__": "jiter_harness"}
        exec(compile((PROJECT / "harness.py").read_text(), "harness.py", "exec"), namespace)
    finally:
        if saved is None:
            sys.modules.pop("jiter")
        else:
            sys.modules["jiter"] = saved
    return namespace["summarize"]


class PythonJsonJiterPilotTest(unittest.TestCase):
    def test_lead_promoted_without_merging_pydantic_family_metric(self):
        parsers = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")["leads"]
        cell = read(BASE / "cell.json")
        names = [parser["name"] for parser in parsers]
        self.assertEqual(names[:2], ["pydantic", "jiter"])
        downloads = {lead["name"]: lead["last_month"] for lead in leads}
        metrics = [downloads[name] for name in names]
        self.assertEqual(metrics, sorted(metrics, reverse=True))
        self.assertEqual(len(parsers), cell["verified_third_party_count"])
        self.assertEqual(sum(lead["status"] == "lead" for lead in leads),
                         cell["unresolved_documentation_leads"])
        lead, = [lead for lead in leads if lead["name"] == "jiter"]
        parser, = [parser for parser in parsers if parser["name"] == "jiter"]
        pydantic, = [parser for parser in parsers if parser["name"] == "pydantic"]
        self.assertEqual(lead["status"], "promoted_to_verified")
        self.assertEqual(lead["last_month"], 421162504)
        self.assertEqual(parser["popularity"]["value"], lead["last_month"])
        # Same Jiter family as Pydantic, kept as a separate package metric.
        self.assertEqual(pydantic["popularity"]["value"], downloads["pydantic"])
        self.assertIn("Jiter", parser["family"])
        self.assertIn("not an independent parser family", parser["family_note"])
        self.assertIn("not combined", parser["popularity"]["limitation"])
        self.assertIn("jiter 0.19.0 (421,162,504)", cell["uncertainty"])
        self.assertIn("not independent parsers", cell["uncertainty"])
        ranking = (BASE / "ranking.md").read_text()
        self.assertIn("| 2 | [jiter]", ranking)
        self.assertNotIn("1,560,592,194", ranking)

    def test_release_lock_matches_manifest_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "jiter"]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        jiter = lock["jiter"]
        self.assertEqual(jiter["release"], manifest["release"])
        self.assertEqual(jiter["sdist_sha256"], manifest["source_sha256"])
        self.assertEqual(parser["source_sha256"], manifest["source_sha256"])
        self.assertEqual(parser["wheel_sha256"], jiter["wheel_sha256"])
        self.assertEqual((parser["license"], jiter["license"]), ("MIT", "MIT"))
        self.assertEqual(jiter["runtime_dependencies"], [])
        self.assertRegex(jiter["upstream_commit"], r"^[0-9a-f]{40}$")
        for digest in (manifest["source_sha256"], jiter["parse_rs_sha256"], jiter["python_rs_sha256"],
                       jiter["string_decoder_rs_sha256"], jiter["number_decoder_rs_sha256"],
                       jiter["python_module_lib_rs_sha256"], jiter["cargo_lock_sha256"],
                       jiter["license_file_sha256"], lock["lexical-parse-float"]["cargo_crate_sha256"]):
            self.assertIn(digest, dockerfile)
        # The Rust JSON cell pins the crates.io crate whose src/ the sdist vendors.
        rust_lock = read(ROOT / "projects/json/rust/jiter/source-lock.json")["jiter"]
        self.assertEqual(rust_lock["release"], lock["jiter_crate"]["release"])
        self.assertEqual(rust_lock["source_sha256"], lock["jiter_crate"]["crates_io_crate_sha256"])
        maturin = lock["build_backend"]["maturin"]
        self.assertIn(f"maturin=={maturin['release']} --hash=sha256:{maturin['wheel_sha256']}",
                      (PROJECT / "build-requirements.lock").read_text())
        self.assertIn("-C instrument-coverage", dockerfile)
        self.assertIn("MATURIN_PEP517_ARGS='--locked'", dockerfile)
        self.assertEqual(manifest["coverage_subject_prefix"], JITER_SRC)
        self.assertEqual(manifest["afl_coverage_subject_prefix"], JITER_SRC)
        self.assertNotIn("jiter-python", manifest["coverage_subject_prefix"])

    def test_expected_summaries_match_controls_under_cpython_json(self):
        manifest = read(PROJECT / "manifest.json")
        summarize = harness_summarize()
        for control, key in (("control", "expected_output"),
                             ("differential_control", "differential_expected_output")):
            source = ROOT / manifest[control]
            observed = json.loads(json.dumps(summarize(json.loads(source.read_bytes()))))
            self.assertEqual(observed, manifest[key], control)
        self.assertEqual(manifest["control"], "controls/json/nested-object.json")
        self.assertEqual(manifest["differential_control"], "controls/json/nested-array.json")
        run_control = (PROJECT / "run-control.py").read_text()
        expected = run_control.split("expected = ", 1)[1].split("\nif observed", 1)[0]
        self.assertEqual(json.loads(json.dumps(eval(expected))), manifest["expected_output"])

    def test_project_receipt_matches_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser, = [item for item in read(BASE / "parsers.json") if item["name"] == "jiter"]
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], parser["expected_output"])
        self.assertEqual(manifest["differential_expected_output"], parser["differential_expected_output"])
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        for control, digest in ((manifest["control"], manifest["control_sha256"]),
                                (manifest["differential_control"], manifest["differential_control_sha256"])):
            self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        record, = [item for item in read(BASE / "verification.json")["third_party"]
                   if item["package"] == "jiter"]
        self.assertEqual(record["project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(record["output"], receipt["output"])
        self.assertEqual(record["native_region_start_lines"], receipt["parser_source_lines_covered"])
        self.assertEqual(record["parse_rs_lines"], receipt["format_specific_source_lines_covered"])

    def test_oracle_and_native_feedback_are_exact_stable_and_differential(self):
        manifest = read(PROJECT / "manifest.json")
        overlay = read(OVERLAY / "verification.json")
        report = read(BASE / "jiter-valid-feedback.json")
        self.assertEqual(overlay["feedback_kind"], "llvm_native_parser_regions_to_afl_bitmap")
        self.assertIn(f"PARSARIUM_SUBJECT_PREFIX={JITER_SRC}", (OVERLAY / "Dockerfile").read_text())
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(report["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        for oracle in (report["control_oracle"], report["variant_oracle"]):
            self.assertTrue(oracle["bytes_matches_oracle"])
            self.assertEqual(oracle["duplicate_keys"], 0)
            self.assertEqual(oracle["jiter"], manifest["release"])
        self.assertNotEqual(report["control_oracle"]["tree_sha256"], report["variant_oracle"]["tree_sha256"])
        self.assertTrue(report["pass"] and report["control_repeat_identical"]
                        and report["variant_repeat_identical"])
        self.assertEqual(report["control_output"], manifest["expected_output"])
        self.assertEqual(report["variant_output"], manifest["differential_expected_output"])
        self.assertEqual((report["control_sha256"], report["variant_sha256"]),
                         (manifest["control_sha256"], manifest["differential_control_sha256"]))
        self.assertGreater(report["parse_rs_feature_difference"], 0)
        self.assertGreater(report["afl_tuple_difference"], 0)
        self.assertEqual(report["value_rs_or_jiter_rs_features"], 0)
        self.assertIn("parse.rs", report["differing_source_files"])
        self.assertTrue(all(not re.search(r"jiter-python|lib\.rs$", name)
                            for name in report["differing_source_files"]))
        self.assertEqual(report["control_parser_features"], overlay["parser_source_features"])
        self.assertEqual(report["control_afl_tuples"], overlay["feedback_edges"])


if __name__ == "__main__":
    unittest.main()
