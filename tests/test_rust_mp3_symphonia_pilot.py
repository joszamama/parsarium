"""The Rust symphonia MP3 facade keeps exact-repeat AFL++ feedback scoped to symphonia-bundle-mp3."""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/mp3/rust/symphonia"
OVERLAY = ROOT / "fuzzing/afl-native/mp3/rust/symphonia"
sys.path.insert(0, str(ROOT / "scripts"))
from build_afl_rust import SCOPE_CHECK, SCOPE_WRAPPER, dockerfile  # noqa: E402

SANCOV = ["-C", "passes=sancov-module", "-C", "llvm-args=-sanitizer-coverage-level=3",
          "-C", "llvm-args=-sanitizer-coverage-trace-pc-guard", "-Cllvm-args=-sanitizer-coverage-trace-compares"]
KEPT = ["-C", "opt-level=3", "--cfg", "fuzzing", "-C", "link-arg=/afl/afl-compiler-rt.o"]


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class RustMp3SymphoniaPilotTest(unittest.TestCase):
    def wrapped_args(self, crate: str) -> tuple[list[str], str]:
        with tempfile.TemporaryDirectory() as temp:
            wrapper, fake = Path(temp) / "wrapper.sh", Path(temp) / "rustc"
            wrapper.write_text(SCOPE_WRAPPER)
            fake.write_text('#!/bin/sh\nprintf "%s\\n" "$@"\n')
            fake.chmod(0o755)
            env = {**os.environ, "AFL_SCOPE_CRATES": "symphonia_bundle_mp3",
                   "AFL_SCOPE_LOG": str(Path(temp) / "scope.log")}
            run = subprocess.run(["bash", str(wrapper), str(fake), "--crate-name", crate, *SANCOV, *KEPT],
                                 env=env, capture_output=True, text=True, check=True)
            return run.stdout.splitlines(), (Path(temp) / "scope.log").read_text()

    def test_wrapper_strips_sancov_outside_scope(self):
        args, log = self.wrapped_args("symphonia_bundle_mp3")
        self.assertEqual(args, ["--crate-name", "symphonia_bundle_mp3", *SANCOV, *KEPT])
        self.assertEqual(log, "instrumented symphonia_bundle_mp3\n")
        for crate in ("symphonia", "symphonia_core", "afl_fuzzer"):
            args, log = self.wrapped_args(crate)
            self.assertEqual(args, ["--crate-name", crate, *KEPT])
            self.assertEqual(log, f"uninstrumented {crate}\n")

    def test_overlay_files_are_generated(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(OVERLAY / "verification.json")
        self.assertEqual(manifest["afl_instrumented_crates"], ["symphonia_bundle_mp3"])
        self.assertEqual((OVERLAY / "rustc-scope.sh").read_text(), SCOPE_WRAPPER)
        self.assertTrue(os.access(OVERLAY / "rustc-scope.sh", os.X_OK))
        self.assertEqual((OVERLAY / "sancov_scope.py").read_text(), SCOPE_CHECK)
        self.assertEqual((OVERLAY / "Dockerfile").read_text(),
                         dockerfile(Path("mp3/rust/symphonia"), manifest, receipt["afl_package"]))
        for name, digest in receipt["overlay_file_sha256"].items():
            self.assertEqual(sha256((OVERLAY / name).read_bytes()).hexdigest(), digest, name)
        self.assertEqual(receipt["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())

    def test_feedback_is_scoped_exact_and_differential(self):
        receipt = read(OVERLAY / "verification.json")
        scope = receipt["sancov_scope"]
        self.assertEqual(scope["instrumented_crates"], ["symphonia_bundle_mp3"])
        self.assertEqual(list(scope["rlib_guard_bytes"]), ["symphonia_bundle_mp3"])
        for crate in ("symphonia", "symphonia_core", "parsarium_mp3_symphonia_harness", "afl"):
            self.assertIn(crate, scope["uninstrumented_rlibs"])
        self.assertLessEqual(scope["binary_guards"] * 4, scope["rlib_guard_bytes"]["symphonia_bundle_mp3"])
        self.assertIn("instrumented symphonia_bundle_mp3", receipt["rustc_wrapper_log"])
        self.assertEqual([line for line in receipt["rustc_wrapper_log"] if line.startswith("instrumented ")],
                         ["instrumented symphonia_bundle_mp3"])
        self.assertGreaterEqual(receipt["repeats"], 3)
        for key, digest, edges in (("control_stability", receipt["control_map_sha256"], receipt["feedback_edges"]),
                                   ("variant_stability", receipt["variant_map_sha256"],
                                    receipt["variant_feedback_edges"])):
            record = receipt[key]
            self.assertTrue(record["all_repeats_identical"])
            self.assertEqual(record["repeat_map_sha256"], [digest] * receipt["repeats"])
            self.assertEqual(record["repeat_tuple_counts"], [edges] * receipt["repeats"])
        self.assertNotIn("stable_edge_rule", receipt)
        self.assertNotEqual(receipt["control_map_sha256"], receipt["variant_map_sha256"])
        self.assertGreater(receipt["edges_only_in_control"], 0)
        self.assertGreater(receipt["edges_only_in_variant"], 0)
        self.assertTrue(receipt["underlying_source_differential"]["files_with_different_line_counts"])

    def test_smoke_rows_match_receipt(self):
        receipt = read(OVERLAY / "verification.json")
        row, = [item for item in read(ROOT / "data/afl-rust-smoke.json")["results"]
                if item["project"] == "mp3/rust/symphonia"]
        self.assertEqual((row["feedback_edges"], row["image_id"]), (receipt["feedback_edges"], receipt["image_id"]))
        plan, = [item for item in read(ROOT / "data/afl-plan-smoke.json")["results"]
                 if item["project"] == "mp3/rust/symphonia"]
        self.assertEqual(plan["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())


if __name__ == "__main__":
    unittest.main()
