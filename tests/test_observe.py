"""Classification and extraction tests for scripts/observe.py (no Docker).

Run: python3 -m unittest discover -s tests
"""

import json
from pathlib import Path
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import observe  # noqa: E402


EXPECTED = {"width": 2, "height": 1}


class ExtractionTests(unittest.TestCase):
    def test_passing_check_uses_summary_output(self):
        files = {"summary.json": json.dumps({"control_pass": True, "output": EXPECTED})}
        record = observe.classify(EXPECTED, 0, "", "", files, False)
        self.assertEqual(record["class"], "accepted")
        self.assertEqual(record["observed"], EXPECTED)
        self.assertEqual(record["observed_route"], "check_passed:summary")
        self.assertTrue(record["matches_control_expected"])

    def test_passing_check_without_summary_falls_back_to_expected(self):
        record = observe.classify(EXPECTED, 0, "{}", "", {}, False)
        self.assertEqual(record["observed_route"], "check_passed:expected_output")
        self.assertEqual(record["observed"], EXPECTED)

    def test_observed_file_wins_after_coverage_failure(self):
        files = {"observed.json": '{"width": 7, "height": 3}\n'}
        record = observe.classify(EXPECTED, 1, "", "llvm-cov: error: failed", files, False)
        self.assertEqual(record["class"], "accepted")
        self.assertEqual(record["observed"], {"width": 7, "height": 3})
        self.assertEqual(record["observed_route"], "file:observed.json")
        self.assertFalse(record["matches_control_expected"])

    def test_observed_raw_reads_last_line(self):
        files = {"observed.raw": "WARNING: loading\n{\"width\": 2, \"height\": 1}\n"}
        record = observe.classify(EXPECTED, 1, "", "jacoco failed", files, False)
        self.assertEqual(record["observed_route"], "file:observed.raw")
        self.assertTrue(record["matches_control_expected"])

    def test_timeout_after_observation_stays_accepted(self):
        files = {"observed.json": '{"width": 9, "height": 9}'}
        record = observe.classify(EXPECTED, None, "", "", files, True)
        self.assertEqual(record["class"], "accepted")
        self.assertTrue(record["timed_out_after_observation"])

    def test_timeout_without_observation(self):
        record = observe.classify(EXPECTED, None, "", "", {}, True)
        self.assertEqual(record, {"class": "timeout"})

    def test_unreachable_daemon_is_a_harness_error(self):
        stderr = "docker: Cannot connect to the Docker daemon at unix:///x/docker.sock."
        record = observe.classify(EXPECTED, 125, "", stderr, {}, False)
        self.assertEqual(record["class"], "harness_error")

    def test_python_repr_message(self):
        stderr = "control mismatch: {'width': 5, 'height': 4, 'alpha': True, 'mode': None, 'px': (1, 2)}\n"
        record = observe.classify(EXPECTED, 1, "", stderr, {}, False)
        self.assertEqual(record["observed"], {"width": 5, "height": 4, "alpha": True,
                                              "mode": None, "px": [1, 2]})
        self.assertEqual(record["observed_route"], "mismatch_message")

    def test_javascript_message_skips_source_line(self):
        stderr = ("/work/run-control.js:19\n"
                  "  throw new Error(`control mismatch: ${JSON.stringify(observed)}`);\n  ^\n\n"
                  'Error: control mismatch: {"width":3,"height":4}\n    at Object.<anonymous>\n')
        record = observe.classify(EXPECTED, 1, "", stderr, {}, False)
        self.assertEqual(record["observed"], {"width": 3, "height": 4})

    def test_php_message_strips_location(self):
        stderr = ('PHP Fatal error:  Uncaught RuntimeException: control mismatch: '
                  '{"width":3,"height":4,"mime":"image\\/png"} in /work/run-control.php:12\nStack trace:\n')
        record = observe.classify(EXPECTED, 255, "", stderr, {}, False)
        self.assertEqual(record["observed"], {"width": 3, "height": 4, "mime": "image/png"})

    def test_go_json_message(self):
        stderr = ("control replay failed: exit status 1: === RUN   TestControl\n"
                  '    harness_test.go:23: control mismatch: {"height":4,"width":3}\n--- FAIL: TestControl\n')
        record = observe.classify(EXPECTED, 1, "", stderr, {}, False, {})
        self.assertEqual(record["observed"], {"height": 4, "width": 3})

    def test_go_message_naming_the_input_path(self):
        stderr = ("control replay failed: exit status 1: === RUN   TestControl\n"
                  '    harness_test.go:32: typed tree mismatch for /input/control: {"tree":["map",[]]}\n--- FAIL: TestControl\n')
        record = observe.classify(EXPECTED, 1, "", stderr, {}, False, {})
        self.assertEqual(record["observed"], {"tree": ["map", []]})

    def test_error_wrapped_by_the_node_runner(self):
        stderr = ("Error: control replay failed: TypeError: Invalid PNM\n"
                  "    at Object.<anonymous> (/work/run-control.js:14:9)\n\nNode.js v24.22.3\n")
        self.assertEqual(observe.parser_error("", stderr, {}), "TypeError: Invalid PNM")

    def test_node_version_trailer_is_not_the_error(self):
        self.assertEqual(observe.parser_error("", "bad header\n\nNode.js v24.22.3\n", {}), "bad header")

    def test_go_struct_message_uses_json_tags(self):
        tags = observe.go_field_tags(['type Result struct {\n\tWidth  int   `json:"width"`\n'
                                      '\tRGBA   []int `json:"rgba"`\n\tName string `json:"name,omitempty"`\n}\n'])
        self.assertEqual(tags, {"Width": "width", "RGBA": "rgba", "Name": "name"})
        stderr = ("    harness_test.go:22: control mismatch: got {Width:3 Height:1 RGBA:[1 2 3 4] Name:x}, "
                  "want {Width:2 Height:1 RGBA:[255 0 0 255] Name:x}\n")
        record = observe.classify(EXPECTED, 1, "", stderr, {}, False, tags)
        self.assertEqual(record["observed"], {"width": 3, "height": 1, "rgba": [1, 2, 3, 4], "name": "x"})

    def test_undecodable_message_is_kept_raw(self):
        stderr = "control mismatch: <Image 3x4 at 0x7f>\n"
        record = observe.classify(EXPECTED, 1, "", stderr, {}, False)
        self.assertEqual(record["class"], "accepted")
        self.assertIsNone(record["observed"])
        self.assertEqual(record["observed_raw"], "<Image 3x4 at 0x7f>")
        self.assertFalse(record["matches_control_expected"])

    def test_disagreeing_message_is_recorded(self):
        files = {"observed.raw": '{"width": 3}'}
        record = observe.classify(EXPECTED, 1, "", "control mismatch: {'width': 3, 'height': 1}", files, False)
        self.assertEqual(record["observed"], {"width": 3})
        self.assertEqual(record["message_observed"], {"width": 3, "height": 1})

    def test_post_comparison_coverage_failure(self):
        record = observe.classify(EXPECTED, 1, "", "SystemExit: no parser package source lines covered", {}, False)
        self.assertEqual(record["class"], "accepted")
        self.assertEqual(record["observed_route"], "post_comparison_failure")
        self.assertTrue(record["matches_control_expected"])


class RejectionTests(unittest.TestCase):
    def test_python_parser_exception(self):
        stderr = ('Traceback (most recent call last):\n  File "/work/run-control.py", line 9\n'
                  "PIL.UnidentifiedImageError: cannot identify image file\n")
        record = observe.classify(EXPECTED, 1, "", stderr, {}, False)
        self.assertEqual(record, {"class": "rejected", "error": "PIL.UnidentifiedImageError: cannot identify image file"})

    def test_go_fatal(self):
        stderr = ("control replay failed: exit status 1: === RUN   TestControl\n"
                  "    harness_test.go:18: png: invalid format: not enough pixel data\n--- FAIL\n")
        record = observe.classify(EXPECTED, 1, "", stderr, {}, False, {})
        self.assertEqual(record["error"], "png: invalid format: not enough pixel data")

    def test_java_exception(self):
        stderr = 'Exception in thread "main" javax.imageio.IIOException: Error reading PNG image data\n\tat x\n'
        record = observe.classify(EXPECTED, 1, "", stderr, {"observed.raw": ""}, False)
        self.assertEqual(record["class"], "rejected")
        self.assertEqual(record["error"], "javax.imageio.IIOException: Error reading PNG image data")

    def test_silent_native_failure(self):
        record = observe.classify(EXPECTED, 5, "", "", {"observed.json": ""}, False)
        self.assertEqual(record, {"class": "rejected", "error": "exit code 5 with no message"})

    def test_invalid_observed_file_reports_its_text(self):
        files = {"observed.json": "Warning: imagecreatefromstring(): gd-png error\n"}
        stderr = "json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)\n"
        record = observe.classify(EXPECTED, 1, "", stderr, files, False)
        self.assertEqual(record["class"], "rejected")

    def test_harness_errors(self):
        self.assertEqual(observe.classify(EXPECTED, 125, "", "Unable to find image", {}, False)["class"],
                         "harness_error")
        self.assertEqual(observe.classify(EXPECTED, 255, "", "PHP Fatal error:  Uncaught RuntimeException: "
                                          "Xdebug coverage extension is missing", {}, False)["class"],
                         "harness_error")
        self.assertEqual(observe.classify(EXPECTED, 137, "", "", {}, False)["class"], "harness_error")


class RecordTests(unittest.TestCase):
    def test_balanced_prefix_honors_strings(self):
        self.assertEqual(observe.balanced_prefix('{"a": "}"} trailing'), '{"a": "}"}')
        self.assertIsNone(observe.balanced_prefix("{unclosed"))

    def test_records_resume_and_sort(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "slug.jsonl"
            rows = [{"input": "b", "input_sha256": "2", "class": "accepted"},
                    {"input": "a", "input_sha256": "1", "class": "timeout"}]
            path.write_text("".join(json.dumps(row) + "\n" for row in rows) + '{"input": "c", "inp')
            records = observe.load_records(path)
            self.assertEqual(sorted(records), [("a", "1"), ("b", "2")])
            observe.write_sorted(path, records)
            self.assertEqual([json.loads(line)["input"] for line in path.read_text().splitlines()], ["a", "b"])

    def test_summary_flags(self):
        records = {("a", "1"): {"class": "accepted", "observed": {"w": 2}},
                   ("b", "2"): {"class": "rejected"}, ("c", "3"): {"class": "rejected"}}
        self.assertTrue(observe.control_only(records, "1"))
        self.assertFalse(observe.control_only(records, "2"))
        same = {(str(i), str(i)): {"class": "accepted", "observed": {"w": 2}} for i in range(3)}
        self.assertTrue(observe.constant_observation(same))
        same[("9", "9")] = {"class": "accepted", "observed": {"w": 3}}
        self.assertFalse(observe.constant_observation(same))

    def test_corpus_files_are_sorted_and_skip_hidden(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "b.png").write_bytes(b"b")
            (root / "a.png").write_bytes(b"a")
            (root / ".DS_Store").write_bytes(b"x")
            self.assertEqual([name for name, _ in observe.corpus_files(root)], ["a.png", "b.png"])


if __name__ == "__main__":
    unittest.main()


class HarnessFrameTests(unittest.TestCase):
    def test_python_adapter_type_error_is_harness_error(self):
        stderr = ('Traceback (most recent call last):\n'
                  '  File "/usr/lib/python3/site-packages/PIL/Image.py", line 9, in getpixel\n'
                  '  File "/work/adapter.py", line 10, in rgba\n'
                  "TypeError: 'int' object is not iterable\n")
        record = observe.classify(EXPECTED, 1, "", stderr, {}, False)
        self.assertEqual(record["class"], "harness_error")
        self.assertIn("/work/adapter.py:10", record["error"])

    def test_python_parser_type_error_is_rejection(self):
        stderr = ('Traceback (most recent call last):\n'
                  '  File "/work/adapter.py", line 10, in run\n'
                  '  File "/usr/local/lib/python3.12/site-packages/png.py", line 9, in read\n'
                  "TypeError: bad chunk\n")
        self.assertEqual(observe.classify(EXPECTED, 1, "", stderr, {}, False)["class"], "rejected")

    def test_javascript_harness_type_error(self):
        stderr = ("Error: control replay failed: /work/harness.js:12\n"
                  "TypeError: Cannot read properties of undefined (reading '0')\n"
                  "    at parsePng (/work/harness.js:12:20)\n")
        self.assertEqual(observe.classify(EXPECTED, 1, "", stderr, {}, False)["class"], "harness_error")

    def test_java_harness_index_error(self):
        stderr = ('Exception in thread "main" java.lang.ArrayIndexOutOfBoundsException: Index 1 out of bounds\n'
                  "\tat GenericHarness.main(GenericHarness.java:30)\n")
        self.assertEqual(observe.classify(EXPECTED, 1, "", stderr, {}, False)["class"], "harness_error")

    def test_java_library_exception_is_rejection(self):
        stderr = ('Exception in thread "main" java.lang.NullPointerException\n'
                  "\tat org.apache.pdfbox.Foo.bar(Foo.java:3)\n")
        self.assertEqual(observe.classify(EXPECTED, 1, "", stderr, {}, False)["class"], "rejected")


class OrderTests(unittest.TestCase):
    def test_unrelated_read_only_warning_does_not_hide_harness_frame(self):
        stderr = ("mkdir -p failed for path /.config/matplotlib: [Errno 30] Read-only file system: '/.config'\n"
                  "Traceback (most recent call last):\n"
                  '  File "/work/adapter.py", line 10, in rgba\n'
                  "TypeError: 'numpy.float32' object is not iterable\n")
        record = observe.classify(EXPECTED, 1, "", stderr, {}, False)
        self.assertEqual(record["class"], "harness_error")
        self.assertIn("summarizing", record["error"])
