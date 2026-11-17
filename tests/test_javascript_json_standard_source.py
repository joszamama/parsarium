"""The Node.js JSON.parse source-coverage route instruments only V8's JSON parser and keeps its receipt honest."""

from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "projects/json/javascript/stdlib_json_parse"
SOURCE = PROJECT / "source-coverage"
OVERLAY = ROOT / "fuzzing/afl-native/json/javascript/stdlib_json_parse"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class NodeJsonSourceCoverageTest(unittest.TestCase):
    def wrapper_args(self, name: str, *args: str, wrapper: Path = SOURCE / "instrument-cc.sh") -> list[str]:
        """Run a compiler wrapper as `name` with a fake clang that prints its arguments."""
        with tempfile.TemporaryDirectory() as work:
            for real in ("clang-20", "clang++-20"):
                fake = Path(work) / real
                fake.write_text('#!/bin/sh\nprintf "%s\\n" "$0" "$@"\n')
                fake.chmod(0o755)
            link = Path(work) / name
            link.symlink_to(wrapper)
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


class NodeJsonParserAflTest(unittest.TestCase):
    def afl_args(self, name: str, *args: str) -> list[str]:
        return NodeJsonSourceCoverageTest.wrapper_args(None, name, *args, wrapper=OVERLAY / "afl-cc.sh")

    def test_afl_wrapper_instruments_only_the_v8_json_parser(self):
        parser = self.afl_args("c++", "-O3", "-c", "../deps/v8/src/json/json-parser.cc", "-o", "json-parser.o")
        self.assertTrue(parser[0].endswith("/clang++-20"))
        self.assertEqual(parser[-1], "-fsanitize-coverage=trace-pc-guard")
        for other in ("../deps/v8/src/json/json-stringifier.cc", "../src/json_parser.cc",
                      "../deps/simdjson/simdjson.cpp"):
            args = self.afl_args("c++", "-c", other, "-o", "x.o")
            self.assertFalse(any(arg.startswith("-fsanitize") for arg in args), other)
            self.assertNotIn("/usr/lib/afl/afl-compiler-rt.o", args)
        link = self.afl_args("c++", "-o", "node", "node_main.o", "libv8_base.a")
        self.assertEqual(link[-1], "/usr/lib/afl/afl-compiler-rt.o")
        self.assertFalse(any(arg.startswith("-fsanitize") for arg in link))
        self.assertNotIn("/usr/lib/afl/afl-compiler-rt.o", self.afl_args("c++", "-shared", "-o", "x.so", "x.o"))
        self.assertNotIn("/usr/lib/afl/afl-compiler-rt.o", self.afl_args("cc", "--version"))

    def test_afl_dockerfile_reuses_the_source_pin_and_gates_one_object(self):
        dockerfile = (OVERLAY / "Dockerfile").read_text()
        manifest = read(PROJECT / "manifest.json")
        feedback = manifest["source_feedback"]
        for pin in ("https://nodejs.org/dist/v26.10.0/node-v26.10.0.tar.xz", feedback["node_source_tarball_sha256"],
                    "clang-20=1:20.1.8-2ubuntu8", feedback["base_image"], manifest["adapter_sha256"],
                    "--v8-enable-temporal-support --without-npm",
                    "afl++=" + manifest["afl_feedback"]["afl_package"],
                    '[ "$(wc -l < /work/instrumented-objects.txt)" = 1 ]',
                    "grep -q '/json-parser\\.o$' /work/instrumented-objects.txt",
                    '[ "$(wc -l < /work/afl-runtime-symbols.txt)" = 3 ]'):
            self.assertIn(pin, dockerfile)
        self.assertNotIn("gdb", dockerfile)
        source = (SOURCE / "Dockerfile").read_text()
        self.assertEqual(source.split("WORKDIR /work\n")[0].split("AS build")[1],
                         dockerfile.split("WORKDIR /work\n")[0].split("AS build")[1])

    def test_afl_receipt_records_parser_only_stable_differential_maps(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(OVERLAY / "verification.json")
        smoke = read(OVERLAY / "plan-smoke.json")
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["feedback_kind"], "v8_json_parser_sancov_edges")
        self.assertIs(receipt["afl_requires_ptrace"], False)
        self.assertIsNone(receipt["source_lines_covered"])
        self.assertEqual(receipt["afl_target"], [*manifest["afl_target"], "@@"])
        self.assertEqual(manifest["afl_target"], ["/opt/node/bin/node", "/work/adapter.mjs"])
        self.assertEqual(receipt["adapter_sha256"], manifest["adapter_sha256"])
        instrumentation = receipt["instrumentation"]
        self.assertEqual(len(instrumentation["instrumented_objects"]), 1)
        self.assertTrue(instrumentation["instrumented_objects"][0].endswith("/deps/v8/src/json/json-parser.o"))
        self.assertEqual(instrumentation["node_sha256"], manifest["afl_feedback"]["instrumented_node_sha256"])
        self.assertNotEqual(instrumentation["node_sha256"], manifest["source_sha256"])
        self.assertNotEqual(instrumentation["node_sha256"], manifest["source_feedback"]["instrumented_node_sha256"])
        maps = receipt["maps"]
        self.assertEqual(maps["tuples"]["baseline"], 0)
        self.assertEqual(maps["tuples"]["decode-only"], 0)
        for control in ("object", "array"):
            self.assertGreater(maps["tuples"][f"{control}-1"], 0)
            self.assertEqual(len({maps["sha256"][f"{control}-{index}"] for index in (1, 2, 3)}), 1)
            self.assertEqual(len({maps["raw_sha256"][f"{control}-{index}"] for index in (1, 2, 3)}), 1)
        self.assertNotEqual(maps["sha256"]["object-1"], maps["sha256"]["array-1"])
        self.assertGreater(maps["object_only_tuples"] + maps["array_only_tuples"], 0)
        self.assertLessEqual(maps["max_tuple_index"], instrumentation["node_guards"] + 8)
        self.assertIn("not source lines", receipt["limit"])
        self.assertEqual(smoke["status"], "ready")
        self.assertIs(smoke["campaign_started"], False)
        self.assertEqual(smoke["afl_target"], receipt["afl_target"])
        self.assertEqual(smoke["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())

    def test_audit_gate_and_inventory_agree(self):
        sys.path.insert(0, str(ROOT / "scripts"))
        from audit_projects import fully_runnable, node_json_native_afl_verified
        path = PROJECT / "manifest.json"
        manifest = read(path)
        self.assertTrue(node_json_native_afl_verified(path, manifest))
        self.assertTrue(fully_runnable(path, manifest))
        broken = {**manifest, "afl_feedback": {**manifest["afl_feedback"], "instrumented_node_sha256": "0" * 64}}
        self.assertFalse(node_json_native_afl_verified(path, broken))
        entry, = read(ROOT / "data/javascript/json/standard.json")["verified_apis"]
        receipt = read(OVERLAY / "verification.json")
        self.assertEqual(entry["afl_feedback"]["kind"], "v8_json_parser_sancov_edges")
        self.assertEqual(entry["afl_feedback"]["object_tuples"], receipt["maps"]["tuples"]["object-1"])
        self.assertEqual(entry["afl_feedback"]["array_tuples"], receipt["maps"]["tuples"]["array-1"])
        self.assertIsNone(entry["parser_source_lines_covered"])


if __name__ == "__main__":
    unittest.main()
