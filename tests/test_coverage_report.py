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
from unittest import mock
import subprocess


ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests/fixtures/coverage_report"
sys.path.insert(0, str(ROOT / "scripts"))

import coverage_report  # noqa: E402
import queue_coverage  # noqa: E402
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

    def report(self, output: Path, sources=None, **options) -> dict:
        if sources is None:
            sources = [("/work/source", self.archive)]
        return coverage_report.build_report(self.root, "png", "c", "demo", self.run_dir,
                                            output, sources, 1, dict(LIMITS), **options)

    def afl_plan(self) -> Path:
        self.run_dir = self.root.parent / "afl-run"
        queue = self.run_dir / "afl-out/default/queue"
        queue.mkdir(parents=True)
        (queue / "id:000000,orig:seed").write_bytes(b"\x89PNG control")
        (queue / "id:000001,orig:valid").write_bytes(b"\x89PNG variant")
        (self.project / "run-control.sh").write_text(
            "llvm-cov export /work/replay -instr-profile=/coverage/control.profdata "
            "> /coverage/coverage.json\n")
        self.receipt["project_file_sha256"]["run-control.sh"] = digest(
            (self.project / "run-control.sh").read_bytes())
        self.write_receipt()
        overlay = self.root / "fuzzing/afl-native/png/c/demo/verification.json"
        overlay.parent.mkdir(parents=True)
        self.write_json(overlay, {"pass": True, "image_id": "sha256:" + "2" * 64,
                                  "base_project_receipt_sha256": digest(
                                      (self.project / "verification.json").read_bytes())})
        self.write_json(self.run_dir / "plan.json", {
            "schema_version": 1, "project": "png/c/demo",
            "source_sha256": self.manifest["source_sha256"],
            "control_sha256": self.manifest["control_sha256"],
            "overlay_receipt_sha256": digest(overlay.read_bytes()),
            "image_id": "sha256:" + "2" * 64, "platform": "linux/arm64",
        })
        return queue


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

    def test_tk_standard_feedback_uses_control_and_decoder_receipts(self):
        run_case.ROOT, run_case.PROJECTS = ROOT, ROOT / "projects"
        evidence = coverage_report.project_evidence(
            ROOT, "png", "python", "stdlib_tkinter_photoimage")
        self.assertTrue(evidence["evidence"]["receipt"].endswith("control-verification.json"))
        self.assertTrue(evidence["feedback"]["afl_overlay"]["matches_project_receipt"])
        self.assertGreater(evidence["feedback"]["afl_overlay"]["feedback_edges"], 0)
        self.assertEqual(coverage_report.coverage_groups(evidence["manifest"])[0][1],
                         "/work/tk/generic/tkImgPNG.c")

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

    def test_prepared_afl_report_is_static_without_replay(self):
        fixture = self.fixture()
        queue = fixture.afl_plan()
        (queue / "id:000002,linked").symlink_to(queue / "id:000000,orig:seed")
        total, picked = queue_coverage.queue_files(fixture.run_dir, 1)
        self.assertEqual((total, len(picked)), (2, 1))
        with mock.patch.object(queue_coverage.subprocess, "run") as docker:
            report = fixture.report(self.base / "report")
            docker.assert_not_called()
        self.assertEqual(report["run"]["kind"], "afl")
        self.assertEqual(report["run"]["queue_inputs_available"], 2)
        self.assertEqual(report["coverage"]["status"], "not_recorded")

    def test_changed_afl_overlay_receipt_is_rejected(self):
        fixture = self.fixture()
        fixture.afl_plan()
        overlay = fixture.root / "fuzzing/afl-native/png/c/demo/verification.json"
        receipt = json.loads(overlay.read_text())
        receipt["image_id"] = "sha256:" + "3" * 64
        fixture.write_json(overlay, receipt)
        with mock.patch.object(queue_coverage.subprocess, "run") as docker:
            with self.assertRaisesRegex(queue_coverage.QueueCoverageError,
                                        "changed since preparation"):
                fixture.report(self.base / "report", queue_replay=True)
            docker.assert_not_called()

    def test_queue_export_objects_accepts_literal_replay_maps(self):
        fixture = self.fixture()
        script = fixture.project / "run-control.sh"
        script.write_text("llvm-cov export /work/replay -object /work/lib/libparser.so "
                          "-instr-profile=/coverage/control.profdata > /coverage/coverage.json\n")
        self.assertEqual(queue_coverage.export_objects(fixture.project),
                         ["/work/lib/libparser.so"])
        script.write_text("llvm-cov export /work/replay -object $(readlink -f /work/lib/libparser.so) "
                          "-instr-profile=/coverage/control.profdata > /coverage/coverage.json\n")
        with self.assertRaisesRegex(queue_coverage.QueueCoverageError, "outside this pilot"):
            queue_coverage.export_objects(fixture.project)
        script.write_text("llvm-cov export /work/replay --summary-only "
                          "-instr-profile=/coverage/control.profdata > /coverage/coverage.json\n")
        self.assertEqual(queue_coverage.export_objects(fixture.project), [])

    def test_bounded_afl_queue_replay_aggregates_llvm_parser_lines(self):
        fixture = self.fixture()
        fixture.afl_plan()
        original = (FIXTURES / "coverage.json").read_bytes()

        def docker(command, **_):
            if command[1:3] == ["image", "inspect"]:
                return subprocess.CompletedProcess(command, 0, f"{IMAGE} linux/arm64\n", "")
            if "/work/replay" in command:
                profile_mount = next(item for item in command if item.endswith(":/profiles"))
                profile_dir = Path(profile_mount.removesuffix(":/profiles"))
                profile = next(item for item in command if item.startswith("LLVM_PROFILE_FILE="))
                prefix = profile.partition("/profiles/")[2].split("-%m")[0]
                (profile_dir / f"{prefix}-fixture.profraw").write_bytes(b"profile")
                return subprocess.CompletedProcess(command, 0)
            output_mount = next(item for item in command if item.endswith(":/coverage"))
            output = Path(output_mount.removesuffix(":/coverage"))
            (output / "aggregate.profdata").write_bytes(b"merged")
            (output / "coverage.json").write_bytes(original)
            return subprocess.CompletedProcess(command, 0)

        with mock.patch.object(queue_coverage.subprocess, "run", side_effect=docker):
            report = fixture.report(self.base / "report", queue_replay=True, queue_limit=2)
        self.assertEqual(report["coverage"]["status"], "llvm_source_lines")
        self.assertEqual(report["coverage"]["groups"][0]["llvm_summary_covered"], 6)
        sample = report["run"]["queue_sample"]
        self.assertEqual(sample["queue_inputs_sampled"], 2)
        self.assertEqual([item["profile_files"] for item in sample["inputs"]], [1, 1])
        self.assertEqual(sample["coverage_image_id"], IMAGE)
        self.assertEqual(sample["profdata_sha256"], digest(b"merged"))
        self.assertIn("bounded AFL++ queue sample", report["coverage"]["statement"])
        self.assertTrue((self.base / "report/files/00001.html").is_file())

    def test_afl_queue_source_scope_and_input_limits_are_honest(self):
        fixture = self.fixture("native_binary_edges")
        queue = fixture.afl_plan()
        report = fixture.report(self.base / "unsupported", queue_replay=True)
        self.assertEqual(report["coverage"]["status"], "unsupported")
        self.assertFalse((self.base / "unsupported/files").exists())
        fixture.manifest["coverage_kind"] = "source_lines"
        fixture.write_json(fixture.project / "manifest.json", fixture.manifest)
        fixture.receipt["project_file_sha256"]["manifest.json"] = digest(
            (fixture.project / "manifest.json").read_bytes())
        fixture.write_receipt()
        overlay = fixture.root / "fuzzing/afl-native/png/c/demo/verification.json"
        overlay_data = json.loads(overlay.read_text())
        overlay_data["base_project_receipt_sha256"] = digest(
            (fixture.project / "verification.json").read_bytes())
        fixture.write_json(overlay, overlay_data)
        plan = fixture.run_dir / "plan.json"
        plan_data = json.loads(plan.read_text())
        plan_data["overlay_receipt_sha256"] = digest(overlay.read_bytes())
        fixture.write_json(plan, plan_data)
        (queue / "id:000002,orig:oversize").write_bytes(b"x" * (run_case.MAX_CASE_BYTES + 1))
        with mock.patch.object(queue_coverage.subprocess, "run", return_value=
                               subprocess.CompletedProcess([], 0, f"{IMAGE} linux/arm64\n", "")):
            with self.assertRaisesRegex(queue_coverage.QueueCoverageError, "exceeds"):
                fixture.report(self.base / "oversize", queue_replay=True, queue_limit=3)

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

    def test_go_executed_lines_show_observations_without_a_denominator(self):
        manifest = {"coverage_subject_prefix": "example.org/parser/"}
        item = {"filename": "example.org/parser/decode.go",
                "executed_lines": [2, 4], "summary": {"lines": {"covered": 2}}}
        coverage = {"data": [{"files": [item]}]}
        files, excluded = coverage_report.source_files(coverage, manifest, [], LIMITS,
                                                        executed_only=True)
        self.assertEqual(excluded, 0)
        self.assertEqual(files[0]["lines"], [[2, True], [4, True]])
        html, truncated = coverage_report.file_page(
            files[0], {"identity": {"package": "parser", "release": "1.0"}}, 10)
        self.assertFalse(truncated)
        self.assertIn("Other lines have no execution information", html)
        self.assertNotIn("mapped lines executed", html)
        item["executed_lines"] = [4, 2]
        with self.assertRaisesRegex(coverage_report.ReportError, "sorted unique"):
            coverage_report.source_files(coverage, manifest, [], LIMITS, executed_only=True)

    def test_executed_lines_render_for_each_exporting_ecosystem(self):
        names = {"python": "Python", "javascript": "JavaScript", "java": "Java",
                 "php": "PHP"}
        for ecosystem, name in names.items():
            with self.subTest(ecosystem=ecosystem):
                base = self.base / ecosystem
                base.mkdir()
                fixture = Fixture(base)
                run_case.ROOT, run_case.PROJECTS = fixture.root, fixture.root / "projects"
                project = fixture.root / "projects/png" / ecosystem / "demo"
                project.parent.mkdir(parents=True)
                fixture.project.rename(project)
                fixture.project = project
                fixture.manifest["ecosystem"] = ecosystem
                fixture.write_json(project / "manifest.json", fixture.manifest)
                fixture.receipt["project_file_sha256"]["manifest.json"] = digest(
                    (project / "manifest.json").read_bytes())
                fixture.receipt["parser_source_files"] = 1
                fixture.receipt["parser_source_lines_covered"] = 2
                fixture.write_receipt()
                fixture.write_json(fixture.run_dir / "summary.json", {
                    "control_pass": True, "output": {"width": 2},
                    "parser_source_files": 1, "parser_source_lines_covered": 2,
                })
                fixture.write_json(fixture.run_dir / "coverage.json", {"data": [{"files": [{
                    "filename": "/work/source/src/sample.c", "executed_lines": [2, 4],
                    "summary": {"lines": {"covered": 2}},
                }]}]})
                output = base / "report"
                report = coverage_report.build_report(
                    fixture.root, "png", ecosystem, "demo", fixture.run_dir, output,
                    [("/work/source", fixture.archive)], 1, dict(LIMITS))
                self.assertEqual(report["coverage"]["status"], f"{ecosystem}_executed_lines")
                self.assertEqual(report["coverage"]["files"][0]["source"]["status"],
                                 "pinned_archive")
                self.assertEqual(report["coverage"]["files"][0]["lines"],
                                 [[2, True], [4, True]])
                self.assertIn(f"Observed {name} parser source", (output / "index.html").read_text())

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
