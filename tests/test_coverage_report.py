"""Fixture tests for scripts/coverage_report.py.

Run: python3 -m unittest discover -s tests
"""

from hashlib import sha256
import io
import json
from pathlib import Path
import sys
import tarfile
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/coverage_report"
sys.path.insert(0, str(ROOT / "scripts"))

import coverage_report  # noqa: E402
import run_case  # noqa: E402


LIMITS = {"max_files": 100, "max_lines": 1000, "max_inputs": 100,
          "max_report_bytes": 16 << 20}
IMAGE = "sha256:" + "1" * 64


def digest(data: bytes) -> str:
    return sha256(data).hexdigest()


class Fixture:
    """A temporary repository with one verified C project and its control run."""

    def __init__(self, base: Path, coverage_kind: str = "source_lines"):
        self.root = base / "repo"
        self.project = self.root / "projects/png/c/demo"
        self.project.mkdir(parents=True)
        control = b"\x89PNG control"
        (self.root / "controls/png").mkdir(parents=True)
        (self.root / "controls/png/control.png").write_bytes(control)
        self.archive = base / "demo-1.0.tar.gz"
        with tarfile.open(self.archive, "w:gz") as archive:
            data = (FIXTURES / "sample.c").read_bytes()
            info = tarfile.TarInfo("demo-1.0/src/sample.c")
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
        self.manifest = {
            "schema_version": 1, "format": "png", "ecosystem": "c", "package": "demo",
            "release": "1.0", "source_sha256": digest(self.archive.read_bytes()),
            "platform": "linux/arm64", "control": "controls/png/control.png",
            "control_sha256": digest(control), "expected_output": {"width": 2},
            "harness": "harness.c", "coverage_subject_prefix": "/work/source/src/",
        }
        if coverage_kind != "source_lines":
            self.manifest["coverage_kind"] = coverage_kind
        (self.project / "harness.c").write_text("int main(void) { return 0; }\n")
        self.write_json(self.project / "manifest.json", self.manifest)
        self.run_dir = base / "run"
        self.run_dir.mkdir()
        coverage = json.loads((FIXTURES / "coverage.json").read_text())
        self.write_json(self.run_dir / "coverage.json", coverage)
        self.write_json(self.run_dir / "summary.json",
                        {"control_pass": True, "output": {"width": 2},
                         "parser_source_files": 2, "parser_source_lines_covered": 6})
        self.receipt = {
            "verified_at_utc": "2026-11-16T00:00:00+00:00", "image_id": IMAGE,
            "platform": "linux/arm64", "toolchain": ["clang 21"],
            "source_sha256": self.manifest["source_sha256"],
            "control_sha256": self.manifest["control_sha256"],
            "project_file_sha256": {name: digest((self.project / name).read_bytes())
                                    for name in ("harness.c", "manifest.json")},
            "output": {"width": 2}, "parser_source_files": 2,
            "parser_source_lines_covered": 6, "pass": True,
        }
        if coverage_kind == "native_binary_edges":
            self.receipt.update({
                "coverage_kind": coverage_kind, "parser_source_files": None,
                "parser_source_lines_covered": None, "coverage_output": None,
                "binding_source_lines_covered": 6,
                "binary_feedback_scope": "underlying_shared_library",
                "binary_feedback": {"feedback_kind": "native_binary_edges_not_source_coverage",
                                    "module": "/opt/lib/libdemo.so", "control_tuples": 191}})
        self.write_receipt()

    @staticmethod
    def write_json(path: Path, value) -> None:
        path.write_text(json.dumps(value, indent=2) + "\n")

    def write_receipt(self) -> None:
        self.write_json(self.project / "verification.json", self.receipt)

    def report(self, output: Path, sources=None) -> dict:
        if sources is None:
            sources = [("/work/source", self.archive)]
        return coverage_report.build_report(self.root, "png", "c", "demo", self.run_dir,
                                            output, sources, 1, dict(LIMITS))


class CoverageReportTest(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name).resolve()
        self.saved = run_case.ROOT, run_case.PROJECTS

    def tearDown(self):
        run_case.ROOT, run_case.PROJECTS = self.saved
        self.temporary.cleanup()

    def fixture(self, coverage_kind: str = "source_lines") -> Fixture:
        fixture = Fixture(self.base, coverage_kind)
        run_case.ROOT, run_case.PROJECTS = fixture.root, fixture.root / "projects"
        return fixture

    def test_segments_map_to_llvm_line_counts(self):
        coverage = json.loads((FIXTURES / "coverage.json").read_text())
        segments = coverage["data"][0]["files"][0]["segments"]
        # Line 4 ("}") inherits the then-block count; line 7 is unmapped;
        # lines 11-13 are a skipped #if 0 region.
        self.assertEqual(coverage_report.line_counts(segments),
                         {1: 1, 2: 1, 3: 1, 4: 1, 5: 0, 6: 0, 8: 0, 9: 0, 10: 0})
        # Several regions starting on one line report the largest count.
        self.assertEqual(coverage_report.line_counts(
            [[1, 1, 5, True, True, False], [1, 10, 9, True, True, False],
             [1, 20, 5, True, False, False], [2, 1, 0, False, False, False]]),
            {1: 9, 2: 5})
        # A gap region alone does not map a line.
        self.assertEqual(coverage_report.line_counts(
            [[1, 1, 0, False, False, False], [2, 1, 4, True, True, True],
             [3, 1, 0, False, False, False]]), {3: 4})

    def test_line_view_uses_parser_files_and_pinned_source(self):
        fixture = self.fixture()
        output = self.base / "report"
        report = fixture.report(output)
        coverage = report["coverage"]
        self.assertEqual(coverage["status"], "llvm_source_lines")
        self.assertEqual(coverage["excluded_files"], 1)
        names = [entry["filename"] for entry in coverage["files"]]
        self.assertNotIn("/work/harness.c", names)
        sample = next(e for e in coverage["files"] if e["filename"].endswith("sample.c"))
        self.assertEqual(sample["segment_lines"], {"mapped": 9, "covered": 4, "uncovered": 5})
        self.assertTrue(sample["segment_summary_agrees"])
        self.assertEqual(sample["source"]["status"], "pinned_archive")
        self.assertEqual(sample["source"]["member"], "demo-1.0/src/sample.c")
        self.assertEqual(sample["source"]["pinned_by"], "source_sha256")
        self.assertEqual(sample["lines"][4], [5, 0])
        self.assertEqual(coverage["groups"][0]["llvm_summary_covered"], 6)
        page = (output / sample["page"]).read_text()
        self.assertIn('<tr class="covered" id="L4"><td class="n">4</td><td class="n">1</td>', page)
        self.assertIn('<tr class="uncovered" id="L5">', page)
        self.assertIn('<tr class="" id="L7"><td class="n">7</td><td class="n"></td>', page)
        stored = json.loads((output / "report.json").read_text())
        self.assertEqual(stored["evidence"]["receipt_sha256"],
                         digest((fixture.project / "verification.json").read_bytes()))
        self.assertNotIn("_text", json.dumps(stored))
        self.assertNotIn("harness.c", (output / "index.html").read_text())

    def test_html_is_escaped(self):
        fixture = self.fixture()
        output = self.base / "report"
        report = fixture.report(output)
        pages = [(output / "index.html").read_text()] + [
            (output / entry["page"]).read_text() for entry in report["coverage"]["files"]]
        combined = "".join(pages)
        self.assertNotIn("<script>", combined)
        self.assertNotIn("<img", combined)
        self.assertIn("&lt;script&gt;alert(1)&lt;/script&gt; &amp; &quot;q&quot;", combined)
        self.assertIn("&quot;&gt;&lt;img src=x onerror=alert(1)&gt;.c", combined)
        self.assertNotIn("‮", combined)
        self.assertIn("&lt;U+202E&gt;", combined)
        odd = next(e for e in report["coverage"]["files"] if "img" in e["filename"])
        self.assertEqual(odd["source"]["status"], "not_in_archive")
        self.assertRegex(odd["page"], r"^files/\d{5}\.html$")

    def test_stale_coverage_is_rejected(self):
        fixture = self.fixture()
        coverage = json.loads((fixture.run_dir / "coverage.json").read_text())
        coverage["data"][0]["files"][0]["summary"]["lines"]["covered"] = 5
        fixture.write_json(fixture.run_dir / "coverage.json", coverage)
        with self.assertRaisesRegex(coverage_report.ReportError, "differs from the verification"):
            fixture.report(self.base / "report")
        self.assertFalse((self.base / "report").exists())

    def test_stale_receipt_is_rejected(self):
        fixture = self.fixture()
        fixture.receipt["parser_source_lines_covered"] = 7
        fixture.write_receipt()
        with self.assertRaisesRegex(coverage_report.ReportError, "differs from the verification"):
            fixture.report(self.base / "report")
        fixture.receipt["parser_source_lines_covered"] = 6
        fixture.write_receipt()
        (fixture.project / "harness.c").write_text("int main(void) { return 1; }\n")
        with self.assertRaisesRegex(ValueError, "changed since verification"):
            fixture.report(self.base / "report")

    def test_unpinned_or_mismatched_source_is_rejected(self):
        fixture = self.fixture()
        other = self.base / "other.tar.gz"
        with tarfile.open(other, "w:gz") as archive:
            info = tarfile.TarInfo("demo-1.0/src/sample.c")
            archive.addfile(info, io.BytesIO(b""))
        with self.assertRaisesRegex(coverage_report.ReportError, "matches no manifest source pin"):
            fixture.report(self.base / "report", [("/work/source", other)])
        # A pinned archive whose file is shorter than the coverage map is not shown.
        short = self.base / "short.tar.gz"
        with tarfile.open(short, "w:gz") as archive:
            data = b"int f(int x) {\n"
            info = tarfile.TarInfo("demo-1.0/src/sample.c")
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
        fixture.manifest["source_sha256"] = digest(short.read_bytes())
        fixture.write_json(fixture.project / "manifest.json", fixture.manifest)
        fixture.receipt["source_sha256"] = fixture.manifest["source_sha256"]
        fixture.receipt["project_file_sha256"]["manifest.json"] = digest(
            (fixture.project / "manifest.json").read_bytes())
        fixture.write_receipt()
        report = fixture.report(self.base / "report", [("/work/source", short)])
        sample = next(e for e in report["coverage"]["files"] if e["filename"].endswith("sample.c"))
        self.assertEqual(sample["source"]["status"], "rejected_line_mismatch")
        self.assertNotIn("return 0;", (self.base / "report" / sample["page"]).read_text())

    def test_binary_edges_report_no_source_lines(self):
        fixture = self.fixture("native_binary_edges")
        output = self.base / "report"
        report = fixture.report(output, [])
        self.assertEqual(report["coverage"]["status"], "binary_edges_only")
        self.assertNotIn("files", report["coverage"])
        self.assertFalse((output / "files").exists())
        index = (output / "index.html").read_text()
        self.assertIn("No parser source-line coverage exists", index)
        self.assertIn("191", index)
        self.assertNotIn("sample.c", index)

    def test_non_llvm_report_separates_underlying_parser_coverage(self):
        fixture = self.fixture()
        fixture.manifest["underlying_coverage_subject_prefix"] = "/work/harness"
        fixture.write_json(fixture.project / "manifest.json", fixture.manifest)
        fixture.receipt["underlying_source_files"] = 1
        fixture.receipt["underlying_source_lines_covered"] = 30
        fixture.receipt["project_file_sha256"]["manifest.json"] = digest(
            (fixture.project / "manifest.json").read_bytes())
        fixture.write_receipt()
        summary = json.loads((fixture.run_dir / "summary.json").read_text())
        summary["underlying_source_files"] = 1
        summary["underlying_source_lines_covered"] = 30
        fixture.write_json(fixture.run_dir / "summary.json", summary)
        coverage = json.loads((fixture.run_dir / "coverage.json").read_text())
        coverage["type"] = "non-llvm.fixture"
        fixture.write_json(fixture.run_dir / "coverage.json", coverage)
        output = self.base / "report"
        report = fixture.report(output, [])
        self.assertEqual(report["coverage"]["status"], "non_llvm_source_lines")
        self.assertEqual([(group["name"], group["covered_lines"])
                          for group in report["coverage"]["groups"]],
                         [("parser", 6), ("underlying", 30)])
        index = (output / "index.html").read_text()
        self.assertIn("underlying source lines", index)
        self.assertIn("Covered source by group", index)
        self.assertFalse((output / "files").exists())

    def test_replay_outcomes_without_input_bytes(self):
        fixture = self.fixture()
        run = self.base / "replay"
        (run / "inputs").mkdir(parents=True)
        (run / "executions").mkdir()
        data = b"<b>SECRET INPUT</b>"
        name = digest(data)
        (run / "inputs" / name).write_bytes(data)
        fixture.write_json(run / "executions" / f"{name}.json",
                           {"sha256": name, "status": "target_nonzero", "exit_code": 1,
                            "image_id": IMAGE, "duration_seconds": 0.5})
        summary = {"schema_version": 1, "project": "png/c/demo",
                   "source_sha256": fixture.manifest["source_sha256"],
                   "control_sha256": fixture.manifest["control_sha256"],
                   "image_ids": [IMAGE], "generator": "Fandango",
                   "original_inputs": [{"path": "<i>a.png</i>", "sha256": name,
                                        "bytes": len(data)}],
                   "unique_inputs": 1, "execution_mode": "per_case",
                   "counts": {"target_nonzero": 1}}
        fixture.write_json(run / "summary.json", summary)
        fixture.run_dir = run
        output = self.base / "report"
        report = fixture.report(output, [])
        self.assertEqual(report["coverage"]["status"], "not_recorded")
        index = (output / "index.html").read_text()
        self.assertIn(name, index)
        self.assertIn("target_nonzero", index)
        self.assertNotIn("SECRET", index + (output / "report.json").read_text())
        self.assertIn("&lt;i&gt;a.png&lt;/i&gt;", index)
        receipt = run / "executions" / f"{name}.json"
        execution = json.loads(receipt.read_text())
        execution["image_id"] = "sha256:" + "2" * 64
        fixture.write_json(receipt, execution)
        with self.assertRaisesRegex(coverage_report.ReportError, "execution receipt used image"):
            fixture.report(self.base / "report2", [])
        execution["image_id"] = IMAGE
        fixture.write_json(receipt, execution)
        summary["image_ids"] = ["sha256:" + "2" * 64]
        fixture.write_json(run / "summary.json", summary)
        with self.assertRaisesRegex(coverage_report.ReportError, "not the verified image"):
            fixture.report(self.base / "report3", [])

    def test_binary_project_replay_does_not_claim_run_coverage(self):
        fixture = self.fixture("native_binary_edges")
        run = self.base / "replay"
        (run / "inputs").mkdir(parents=True)
        (run / "executions").mkdir()
        data = b"valid fixture input"
        name = digest(data)
        (run / "inputs" / name).write_bytes(data)
        fixture.write_json(run / "executions" / f"{name}.json",
                           {"sha256": name, "status": "ok", "image_id": IMAGE})
        fixture.write_json(run / "summary.json", {
            "schema_version": 1, "project": "png/c/demo",
            "source_sha256": fixture.manifest["source_sha256"],
            "control_sha256": fixture.manifest["control_sha256"],
            "image_ids": [IMAGE],
            "original_inputs": [{"path": "control.png", "sha256": name,
                                 "bytes": len(data)}],
            "unique_inputs": 1, "execution_mode": "per_case", "counts": {"ok": 1}})
        fixture.run_dir = run
        output = self.base / "report"
        report = fixture.report(output, [])
        self.assertEqual(report["coverage"]["status"], "not_recorded")
        self.assertFalse((output / "files").exists())
        self.assertIn("Replay runs record outcomes only", (output / "index.html").read_text())

    def test_output_directory_is_bounded(self):
        fixture = self.fixture()
        for target in (fixture.run_dir / "report", fixture.root / "website/report",
                       fixture.project / "report"):
            with self.assertRaises(coverage_report.ReportError):
                fixture.report(target)
        (self.base / "used").mkdir()
        (self.base / "used/keep.txt").write_text("keep")
        with self.assertRaisesRegex(coverage_report.ReportError, "new or empty"):
            fixture.report(self.base / "used")

    def test_report_size_limit_truncates_line_views(self):
        fixture = self.fixture()
        output = self.base / "report"
        report = coverage_report.build_report(
            fixture.root, "png", "c", "demo", fixture.run_dir, output,
            [("/work/source", fixture.archive)], 1, {**LIMITS, "max_files": 1})
        self.assertEqual(sum(1 for e in report["coverage"]["files"] if e["page"]), 1)
        self.assertEqual(len(list((output / "files").iterdir())), 1)
        self.assertTrue(report["truncated"])

    def test_report_size_limit_rejects_oversized_index_and_json(self):
        fixture = self.fixture()
        output = self.base / "too-small"
        with self.assertRaisesRegex(coverage_report.ReportError, "above the .*byte limit"):
            coverage_report.build_report(
                fixture.root, "png", "c", "demo", fixture.run_dir, output,
                [("/work/source", fixture.archive)], 1,
                {**LIMITS, "max_report_bytes": 4096})
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
