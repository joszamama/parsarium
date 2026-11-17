"""The Node.js JSON.parse source-coverage route instruments only V8's JSON parser and keeps its receipt honest."""

import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/json/javascript/stdlib_json_parse"
SOURCE = PROJECT / "source-coverage"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class NodeJsonSourceCoverageTest(unittest.TestCase):
    def wrapper_args(self, name: str, *args: str) -> list[str]:
        """Run instrument-cc.sh as `name` with a fake clang that prints its arguments."""
        with tempfile.TemporaryDirectory() as work:
            for real in ("clang-20", "clang++-20"):
                fake = Path(work) / real
                fake.write_text('#!/bin/sh\nprintf "%s\\n" "$0" "$@"\n')
                fake.chmod(0o755)
            link = Path(work) / name
            link.symlink_to(SOURCE / "instrument-cc.sh")
            output = subprocess.run([str(link), *args], check=True, capture_output=True, text=True,
                                    env={**os.environ, "PATH": f"{work}:/usr/bin:/bin"}).stdout
        return output.splitlines()

    def test_wrapper_instruments_only_the_v8_json_parser(self):
        parser = self.wrapper_args("c++", "-O3", "-c", "../deps/v8/src/json/json-parser.cc", "-o", "json-parser.o")
        self.assertTrue(parser[0].endswith("/clang++-20"))
        self.assertEqual(parser[-2:], ["-fprofile-instr-generate", "-fcoverage-mapping"])
        for other in ("../deps/v8/src/json/json-stringifier.cc", "../src/json_parser.cc",
                      "../deps/simdjson/simdjson.cpp"):
            args = self.wrapper_args("c++", "-c", other, "-o", "x.o")
            self.assertNotIn("-fprofile-instr-generate", args)
            self.assertNotIn("-fcoverage-mapping", args)
        link = self.wrapper_args("c++", "-o", "node", "node_main.o", "libv8_base.a")
        self.assertEqual(link[-1], "-fprofile-instr-generate")
        self.assertNotIn("-fcoverage-mapping", link)
        self.assertNotIn("-fprofile-instr-generate", self.wrapper_args("cc", "--version"))
        self.assertTrue(self.wrapper_args("cc", "--version")[0].endswith("/clang-20"))

    def test_dockerfile_pins_official_source_and_toolchain(self):
        dockerfile = (SOURCE / "Dockerfile").read_text()
        manifest = read(PROJECT / "manifest.json")
        feedback = manifest["source_feedback"]
        self.assertIn("https://nodejs.org/dist/v26.10.0/node-v26.10.0.tar.xz", dockerfile)
        self.assertIn(feedback["node_source_tarball_sha256"], dockerfile)
        self.assertIn("clang-20=1:20.1.8-2ubuntu8", dockerfile)
        self.assertIn("llvm-20=1:20.1.8-2ubuntu8", dockerfile)
        self.assertIn(feedback["base_image"], dockerfile)
        self.assertIn(manifest["adapter_sha256"], dockerfile)
        self.assertIn(manifest["differential_control_sha256"], dockerfile)
        self.assertIn("--v8-enable-temporal-support", dockerfile)
        self.assertIn('[ "$(wc -l < /work/instrumented-objects.txt)" = 1 ]', dockerfile)
        self.assertEqual(manifest["source_feedback_smoke"], "source-coverage/run-smoke.sh")

    def test_receipt_records_stable_input_dependent_parser_lines(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        feedback = receipt["source_feedback"]
        expected = manifest["source_feedback"]
        self.assertEqual(feedback["feedback_kind"], "llvm_source_lines")
        self.assertEqual(len(feedback["instrumented_objects"]), 1)
        self.assertTrue(feedback["instrumented_objects"][0].endswith("/deps/v8/src/json/json-parser.o"))
        self.assertTrue(feedback["image_id"].startswith("sha256:"))
        self.assertEqual(feedback["source_sha256"], expected["source_sha256"])
        self.assertEqual(feedback["node_sha256"], expected["instrumented_node_sha256"])
        self.assertEqual(feedback["adapter_sha256"], manifest["adapter_sha256"])
        self.assertEqual(feedback["control_sha256"], {
            "/controls/nested-object.json": manifest["control_sha256"],
            "/controls/nested-array.json": manifest["differential_control_sha256"]})
        self.assertIn("v26.10.0", feedback["toolchain"])
        self.assertIn("v8 " + manifest["v8"], feedback["toolchain"])
        runs = feedback["runs"]
        self.assertEqual(runs["baseline"]["lines_covered"], 0)
        self.assertEqual(runs["decode-only"]["lines_covered"], 0)
        self.assertIsNone(runs["baseline"]["output_matches_expected"])
        for name in ("object-1", "object-2", "array-1", "array-2"):
            self.assertTrue(runs[name]["output_matches_expected"])
            self.assertGreater(runs[name]["lines_covered"], 0)
            self.assertLessEqual(runs[name]["lines_covered"], feedback["scope_lines"])
        for key in ("object_repeat_identical_lines", "object_repeat_identical_counts",
                    "array_repeat_identical_lines", "array_repeat_identical_counts",
                    "object_array_lines_differ"):
            self.assertIs(feedback[key], True, key)
        self.assertTrue(feedback["object_only_lines"] or feedback["array_only_lines"])
        self.assertNotEqual(runs["object-1"]["line_set_sha256"], runs["array-1"]["line_set_sha256"])
        self.assertEqual(runs["object-1"]["line_counts_sha256"], runs["object-2"]["line_counts_sha256"])
        self.assertEqual(receipt["coverage_kind"], "native_function_entries")
        self.assertIsNone(receipt["parser_source_lines_covered"])

    def test_inventory_names_the_source_built_runtime(self):
        entry, = read(ROOT / "data/javascript/json/standard.json")["verified_apis"]
        receipt = read(PROJECT / "verification.json")["source_feedback"]
        self.assertEqual(entry["source_feedback"]["kind"], "llvm_source_lines")
        self.assertEqual(entry["source_feedback"]["object_lines_covered"], receipt["runs"]["object-1"]["lines_covered"])
        self.assertEqual(entry["source_feedback"]["array_lines_covered"], receipt["runs"]["array-1"]["lines_covered"])
        self.assertIn("source-built", entry["source_feedback"]["runtime"])


if __name__ == "__main__":
    unittest.main()
