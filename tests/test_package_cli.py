"""Regression tests for saved selections and snapshot fetch failures."""

from __future__ import annotations

import contextlib
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from parsarium import catalog, cli, selection, snapshot  # noqa: E402


class CatalogTests(unittest.TestCase):
    def test_standard_runtime_is_release_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            project = root / "projects/png/python/stdlib_example"
            project.mkdir(parents=True)
            (project / "manifest.json").write_text(json.dumps({
                "kind": "standard", "package": "stdlib.Example",
                "runtime": "CPython 3.13.1 with bundled Tk 8.6",
                "control": "controls/png/example.png",
            }))
            with mock.patch.object(catalog, "_runnable_check", return_value=lambda *_: True):
                found = catalog._load(root)
            self.assertEqual(len(found), 1)
            self.assertEqual(found[0].release, "CPython 3.13.1 with bundled Tk 8.6")


class SelectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "snapshot"
        project = self.root / "projects/png/python/demo"
        project.mkdir(parents=True)
        control = self.root / "controls/png/control.png"
        control.parent.mkdir(parents=True)
        control.write_bytes(b"valid-control")
        (self.root / "parsarium.py").write_text("# test snapshot\n")
        (self.root / "parsarium-snapshot.json").write_text(json.dumps({"commit": "a" * 40}))
        (project / "manifest.json").write_text(json.dumps({
            "format": "png", "ecosystem": "python", "package": "Demo",
            "release": "1.2.3", "control": "controls/png/control.png",
        }))
        self.saved = {
            "schema": "parsarium-selection/1", "id": "sel-example", "commit": "a" * 8,
            "targets": [{
                "id": "png/python/demo", "format": "png", "ecosystem": "python",
                "package": "Demo", "release": "1.2.3", "control": "controls/png/control.png",
            }],
        }
        self.manifest = Path(self.temp.name) / "selection.json"
        self.out = Path(self.temp.name) / "results"

    def save(self) -> None:
        self.manifest.write_text(json.dumps(self.saved))

    def dry_run(self, allow_mismatch: bool = False) -> tuple[int, str, str]:
        stdout, stderr = io.StringIO(), io.StringIO()
        with mock.patch.object(selection.subprocess, "call") as run, \
             contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = selection.run(self.manifest, self.root, "control", None,
                                   self.out, 10, dry_run=True,
                                   allow_mismatch=allow_mismatch)
            run.assert_not_called()
        return result, stdout.getvalue(), stderr.getvalue()

    def test_matching_pins_dry_run(self) -> None:
        self.save()
        result, output, warnings = self.dry_run()
        self.assertEqual(result, 0)
        self.assertIn(str(self.root / "controls/png/control.png"), output)
        self.assertEqual(warnings, "")
        self.assertFalse(self.out.exists())

    def test_changed_release_fails_before_running(self) -> None:
        self.saved["targets"][0]["release"] = "9.9.9"
        self.save()
        with mock.patch.object(selection.subprocess, "call") as run, \
             contextlib.redirect_stdout(io.StringIO()) as output:
            with self.assertRaisesRegex(ValueError, "release"):
                selection.run(self.manifest, self.root, "control", None,
                              self.out, 10, dry_run=True)
            run.assert_not_called()
            self.assertEqual(output.getvalue(), "")

    def test_changed_commit_has_nonzero_cli_exit(self) -> None:
        self.saved["commit"] = "b" * 8
        self.save()
        stderr = io.StringIO()
        with mock.patch.object(cli, "home", return_value=self.root), \
             contextlib.redirect_stderr(stderr), \
             contextlib.redirect_stdout(io.StringIO()), \
             mock.patch.object(selection.subprocess, "call") as run:
            result = cli.main(["run-selection", str(self.manifest), "--dry-run"])
            run.assert_not_called()
        self.assertEqual(result, 2)
        self.assertIn("pins commit", stderr.getvalue())

    def test_override_reports_mismatches_and_uses_current_control(self) -> None:
        self.saved["commit"] = "b" * 8
        target = self.saved["targets"][0]
        target["release"] = "9.9.9"
        target["control"] = "controls/png/obsolete.png"
        self.save()
        result, output, warnings = self.dry_run(allow_mismatch=True)
        self.assertEqual(result, 0)
        self.assertIn("pins commit", warnings)
        self.assertIn("release:", warnings)
        self.assertIn("control:", warnings)
        self.assertIn(str(self.root / "controls/png/control.png"), output)
        self.assertNotIn("obsolete.png", output)


class HomeTests(unittest.TestCase):
    def test_fetch_http_404_has_nonzero_exit(self) -> None:
        info = {"version": "test", "url": "https://example.invalid/snapshot.tar.gz",
                "sha256": "0" * 64, "bundle": None}
        error = urllib.error.HTTPError(info["url"], 404, "Not Found", {}, None)
        stderr = io.StringIO()
        with tempfile.TemporaryDirectory() as cache, \
             mock.patch.dict(os.environ, {"PARSARIUM_HOME": ""}), \
             mock.patch.object(snapshot, "snapshot_info", return_value=info), \
             mock.patch.object(cli, "snapshot_info", return_value=info), \
             mock.patch.object(snapshot, "cache_root", return_value=Path(cache)), \
             mock.patch.object(snapshot.urllib.request, "urlopen", side_effect=error), \
             contextlib.redirect_stderr(stderr):
            result = cli.main(["home", "--fetch"])
        self.assertEqual(result, 2)
        self.assertIn("404", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
