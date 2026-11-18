"""Tests for the installable package: snapshot install, catalog API, CLI, selections.

These run without Docker or network access. Snapshots are small tarballs built
in a temporary directory and installed through the same code path a release
wheel uses.
"""

from __future__ import annotations

import contextlib
import hashlib
import io
import json
import os
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from parsarium import __version__, catalog, cli, selection, snapshot  # noqa: E402


def _tarball(path: Path, entries: dict[str, bytes | None], links: dict[str, str] | None = None) -> str:
    """Write a gzip tarball; None values are directories. Return its SHA-256."""
    with tarfile.open(path, "w:gz") as archive:
        for name, data in entries.items():
            info = tarfile.TarInfo(name)
            if data is None:
                info.type = tarfile.DIRTYPE
                info.mode = 0o755
                archive.addfile(info)
            else:
                info.size = len(data)
                info.mode = 0o644
                archive.addfile(info, io.BytesIO(data))
        for name, target in (links or {}).items():
            info = tarfile.TarInfo(name)
            info.type = tarfile.SYMTYPE
            info.linkname = target
            archive.addfile(info)
    return hashlib.sha256(path.read_bytes()).hexdigest()


GOOD = {"parsarium-test": None, "parsarium-test/parsarium.py": b"# snapshot entry\n",
        "parsarium-test/data": None, "parsarium-test/data/note.txt": b"ok\n"}


class SnapshotInstallTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.cache = self.base / "cache"
        self.tarball = self.base / "snapshot.tar.gz"
        patches = [mock.patch.dict(os.environ, {"PARSARIUM_HOME": "", "PARSARIUM_SNAPSHOT_URL": "",
                                                "PARSARIUM_CACHE": str(self.cache)})]
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)

    def info(self, sha: str, **extra) -> dict:
        return {"version": "test", "prefix": "parsarium-test", "url": str(self.tarball),
                "sha256": sha, "bundle": None, **extra}

    def install(self, info: dict) -> Path:
        with mock.patch.object(snapshot, "snapshot_info", return_value=info), \
             contextlib.redirect_stderr(io.StringIO()):
            return snapshot.home(fetch=True)

    def test_installs_verified_snapshot_and_reuses_cache(self) -> None:
        sha = _tarball(self.tarball, GOOD)
        path = self.install(self.info(sha))
        self.assertEqual(path, (self.cache / "test").resolve())
        self.assertEqual((path / "data/note.txt").read_text(), "ok\n")
        self.tarball.unlink()  # a second call must not need the archive
        self.assertEqual(self.install(self.info(sha)), path)

    def test_checksum_mismatch_leaves_no_snapshot(self) -> None:
        _tarball(self.tarball, GOOD)
        with self.assertRaisesRegex(snapshot.SnapshotError, "checksum mismatch"):
            self.install(self.info("0" * 64))
        self.assertFalse((self.cache / "test").exists())
        self.assertEqual([p.name for p in self.cache.iterdir()], [])  # temp workspace removed

    def test_rejects_paths_outside_prefix(self) -> None:
        sha = _tarball(self.tarball, {**GOOD, "elsewhere.txt": b"x"})
        with self.assertRaisesRegex(snapshot.SnapshotError, "unexpected path"):
            self.install(self.info(sha))

    def test_rejects_parent_traversal(self) -> None:
        sha = _tarball(self.tarball, {**GOOD, "parsarium-test/../escape.txt": b"x"})
        with self.assertRaisesRegex(snapshot.SnapshotError, "unsafe path"):
            self.install(self.info(sha))
        self.assertFalse((self.cache / "escape.txt").exists())

    def test_rejects_absolute_and_escaping_links(self) -> None:
        for link in ("/etc/passwd", "../../outside"):
            with self.subTest(link=link):
                sha = _tarball(self.tarball, GOOD, {"parsarium-test/data/link": link})
                with self.assertRaisesRegex(snapshot.SnapshotError, "unsafe link"):
                    self.install(self.info(sha))

    def test_allows_links_inside_the_snapshot(self) -> None:
        sha = _tarball(self.tarball, GOOD, {"parsarium-test/data/alias.txt": "note.txt"})
        path = self.install(self.info(sha))
        self.assertEqual((path / "data/alias.txt").read_text(), "ok\n")

    def test_requires_entry_point(self) -> None:
        sha = _tarball(self.tarball, {"parsarium-test": None, "parsarium-test/README.md": b"x"})
        with self.assertRaisesRegex(snapshot.SnapshotError, "does not contain parsarium.py"):
            self.install(self.info(sha))

    def test_bundled_archive_is_hashed_and_installed(self) -> None:
        bundle_dir = self.base / "package"
        bundle_dir.mkdir()
        sha = _tarball(bundle_dir / "_snapshot.tar.gz", GOOD)
        info = self.info(sha, bundle="_snapshot.tar.gz", url=None)
        with mock.patch.object(snapshot.resources, "files", return_value=bundle_dir):
            path = self.install(info)
        self.assertTrue((path / "parsarium.py").is_file())

    def test_missing_bundle_is_reported(self) -> None:
        info = self.info("0" * 64, bundle="_snapshot.tar.gz", url=None)
        with mock.patch.object(snapshot.resources, "files", return_value=self.base / "empty"):
            with self.assertRaisesRegex(snapshot.SnapshotError, "archive is missing"):
                self.install(info)

    def test_without_fetch_or_release_pin(self) -> None:
        with mock.patch.object(snapshot, "snapshot_info", return_value=self.info("0" * 64)):
            with self.assertRaisesRegex(snapshot.SnapshotError, "home --fetch"):
                snapshot.home(fetch=False)
        with self.assertRaisesRegex(snapshot.SnapshotError, "development install"):
            self.install({"version": "test", "bundle": None, "url": None, "sha256": None})

    def test_remove_deletes_cached_version(self) -> None:
        sha = _tarball(self.tarball, GOOD)
        path = self.install(self.info(sha))
        with mock.patch.object(snapshot, "snapshot_info", return_value=self.info(sha)):
            self.assertEqual(snapshot.remove().resolve(), path)
        self.assertFalse(path.exists())


class SnapshotSettingsTests(unittest.TestCase):
    def test_home_override_must_contain_entry_point(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            with mock.patch.dict(os.environ, {"PARSARIUM_HOME": temp}):
                with self.assertRaisesRegex(snapshot.SnapshotError, "does not contain"):
                    snapshot.home()
                (Path(temp) / "parsarium.py").write_text("")
                self.assertEqual(snapshot.home(), Path(temp).resolve())

    def test_url_override_replaces_bundle(self) -> None:
        env = {"PARSARIUM_SNAPSHOT_URL": "https://example.invalid/s.tar.gz",
               "PARSARIUM_SNAPSHOT_SHA256": "f" * 64}
        with mock.patch.dict(os.environ, env):
            info = snapshot.snapshot_info()
        self.assertEqual((info["url"], info["sha256"], info["bundle"]), (env["PARSARIUM_SNAPSHOT_URL"], "f" * 64, None))

    def test_cache_root_per_platform(self) -> None:
        with mock.patch.dict(os.environ, {"PARSARIUM_CACHE": "/tmp/pc"}):
            self.assertEqual(snapshot.cache_root(), Path("/tmp/pc"))
        with mock.patch.dict(os.environ, {"PARSARIUM_CACHE": "", "XDG_CACHE_HOME": "/xdg"}), \
             mock.patch.object(snapshot.sys, "platform", "linux"), mock.patch.object(snapshot.os, "name", "posix"):
            self.assertEqual(snapshot.cache_root(), Path("/xdg/parsarium"))
        with mock.patch.dict(os.environ, {"PARSARIUM_CACHE": ""}), \
             mock.patch.object(snapshot.sys, "platform", "darwin"):
            self.assertEqual(snapshot.cache_root(), Path.home() / "Library/Caches/parsarium")

    def test_released_package_pins_its_snapshot(self) -> None:
        info = json.loads((Path(snapshot.__file__).parent / "_snapshot.json").read_text())
        self.assertIn("version", info)
        if info.get("sha256"):  # release builds only
            self.assertRegex(info["sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(info["version"], __version__)


class CatalogApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for fmt, eco in (("png", "c"), ("json", "rust")):
            (self.root / f"data/{eco}/{fmt}").mkdir(parents=True)
            (self.root / f"data/{eco}/{fmt}/cell.json").write_text("{}")
        (self.root / "data/c/png/parsers.json").write_text(json.dumps([
            {"name": "libpng", "family": "libpng", "input_api": "png_read_png"}]))
        self.project("png", "c", "libpng", {"package": "libpng", "release": "1.6.50",
                                            "catalog_parser": "data/c/png/parsers.json"})
        self.project("json", "rust", "serde_json", {"package": "serde_json", "release": "1.0"})
        self.project("json", "rust", "broken", {"package": "broken", "release": "0.1", "runnable": False})
        catalog._load.cache_clear()
        self.addCleanup(catalog._load.cache_clear)
        runnable = mock.patch.object(catalog, "_runnable_check",
                                     return_value=lambda _path, manifest: manifest.get("runnable", True))
        homed = mock.patch.object(catalog, "home", return_value=self.root)
        for patch in (runnable, homed):
            patch.start()
            self.addCleanup(patch.stop)

    def project(self, fmt: str, eco: str, slug: str, manifest: dict) -> None:
        path = self.root / f"projects/{fmt}/{eco}/{slug}"
        path.mkdir(parents=True)
        (path / "manifest.json").write_text(json.dumps({"control": f"controls/{fmt}/x", **manifest}))

    def test_filters_and_catalog_metadata(self) -> None:
        self.assertEqual([t.id for t in catalog.targets()], ["json/rust/serde_json", "png/c/libpng"])
        png = catalog.targets(format="png")
        self.assertEqual(len(png), 1)
        self.assertEqual((png[0].family, png[0].input_api), ("libpng", "png_read_png"))
        self.assertEqual([t.slug for t in catalog.targets(ecosystem="rust")], ["serde_json"])
        self.assertEqual(catalog.target("png/c/libpng").release, "1.6.50")
        self.assertEqual(catalog.control_path(png[0]), self.root / "controls/png/x")

    def test_rejects_unknown_names(self) -> None:
        with self.assertRaisesRegex(ValueError, "unknown format"):
            catalog.targets(format="gif")
        with self.assertRaisesRegex(ValueError, "unknown ecosystem"):
            catalog.targets(ecosystem="cobol")
        with self.assertRaises(KeyError):
            catalog.target("json/rust/broken")

    def test_format_aliases_map_project_directories(self) -> None:
        (self.root / "data/formats.json").write_text(json.dumps({"formats": [
            {"id": "mp3", "project_formats": ["mp3", "mp3_old"]}]}))
        aliases = catalog._format_aliases(self.root)
        self.assertEqual(aliases, {"mp3": "mp3", "mp3_old": "mp3"})
        self.assertEqual(catalog._data_path("data/c/mp3_old/parsers.json", aliases), "data/c/mp3/parsers.json")

    def test_target_without_release_is_an_error(self) -> None:
        self.project("png", "c", "norelease", {"package": "x"})
        with self.assertRaisesRegex(ValueError, "no release or runtime"):
            catalog.targets()


class CliTests(unittest.TestCase):
    def run_cli(self, *argv: str) -> tuple[int, str, str]:
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = cli.main(list(argv))
        return code, out.getvalue(), err.getvalue()

    def test_help_and_version(self) -> None:
        code, out, _ = self.run_cli()
        self.assertEqual(code, 0)
        self.assertIn("run-selection", out)
        info = {"version": "snap", "commit": "abc"}
        with mock.patch.object(cli, "snapshot_info", return_value=info):
            code, out, _ = self.run_cli("--version")
        self.assertEqual((code, out.strip()), (0, f"parsarium {__version__} (snapshot snap, commit abc)"))

    def test_home_reports_uncached_snapshot_without_failing(self) -> None:
        with mock.patch.object(cli, "snapshot_info", return_value={"version": "snap"}), \
             mock.patch.object(cli, "home", side_effect=snapshot.SnapshotError("no snapshot")):
            code, out, _ = self.run_cli("home")
            self.assertEqual(code, 0)
            self.assertIn("not cached", out)
            code, _, err = self.run_cli("home", "--path")
            self.assertEqual(code, 2)
            self.assertIn("no snapshot", err)

    def test_home_path_and_remove(self) -> None:
        with mock.patch.object(cli, "snapshot_info", return_value={"version": "snap"}), \
             mock.patch.object(cli, "home", return_value=Path("/snap/home")):
            self.assertEqual(self.run_cli("home", "--path")[1].strip(), "/snap/home")
        with mock.patch.object(cli, "remove", return_value=Path("/cache/snap")):
            self.assertEqual(self.run_cli("home", "--remove")[1].strip(), "removed /cache/snap")

    def test_other_commands_run_the_snapshot_entry_point(self) -> None:
        with mock.patch.object(cli, "home", return_value=Path("/snap")), \
             mock.patch.object(cli.subprocess, "call", return_value=3) as call:
            code, _, _ = self.run_cli("list", "--format", "png")
        self.assertEqual(code, 3)
        call.assert_called_once_with([sys.executable, "/snap/parsarium.py", "list", "--format", "png"])


class SelectionModeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        base = Path(self.temp.name)
        self.root = base / "snapshot"
        (self.root / "controls/png").mkdir(parents=True)
        (self.root / "controls/png/c.png").write_bytes(b"x")
        (self.root / "parsarium.py").write_text("")
        (self.root / "parsarium-snapshot.json").write_text(json.dumps({"commit": "c" * 40}))
        targets = []
        for slug in ("one", "two"):
            project = self.root / f"projects/png/python/{slug}"
            project.mkdir(parents=True)
            manifest = {"format": "png", "ecosystem": "python", "package": slug,
                        "release": "1", "control": "controls/png/c.png"}
            (project / "manifest.json").write_text(json.dumps(manifest))
            targets.append({"id": f"png/python/{slug}", **manifest})
        self.manifest = base / "sel.json"
        self.manifest.write_text(json.dumps({"schema": "parsarium-selection/1", "id": "sel-x",
                                             "commit": "c" * 8, "targets": targets}))
        self.inputs = base / "inputs"
        self.inputs.mkdir()
        (self.inputs / "a.png").write_bytes(b"a")
        (self.inputs / "b.png").write_bytes(b"b")
        self.out = base / "out"

    def dry(self, mode: str, input_path: Path | None = None) -> list[str]:
        out = io.StringIO()
        with mock.patch.object(selection.subprocess, "call") as call, contextlib.redirect_stdout(out):
            self.assertEqual(selection.run(self.manifest, self.root, mode, input_path, self.out, 60,
                                           dry_run=True), 0)
            call.assert_not_called()
        return [line.strip() for line in out.getvalue().splitlines() if line.startswith("   ")]

    def test_dry_run_commands_per_mode(self) -> None:
        self.assertEqual(len(self.dry("file", self.inputs)), 4)  # two files x two targets
        replay = self.dry("replay", self.inputs)
        self.assertTrue(all(cmd.startswith("parsarium replay png python") for cmd in replay))
        afl = self.dry("afl")
        self.assertEqual([cmd.split()[2] for cmd in afl[:4]], ["build", "prepare", "run", "summary"])
        self.assertIn("--seconds 60", afl[2])

    def test_file_and_replay_need_input(self) -> None:
        for mode in ("file", "replay"):
            with self.assertRaisesRegex(ValueError, "--input is required"):
                selection.run(self.manifest, self.root, mode, None, self.out, 60, dry_run=True)

    def test_failures_are_recorded_and_stop_that_target(self) -> None:
        calls = []

        def fake_call(command):
            calls.append(command)
            return 1 if "one" in command and "prepare" in command else 0

        with mock.patch.object(selection.subprocess, "call", side_effect=fake_call), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            code = selection.run(self.manifest, self.root, "afl", None, self.out, 5)
        self.assertEqual(code, 1)
        self.assertEqual((self.out / "failed.txt").read_text(), "png/python/one\n")
        one = [c for c in calls if "one" in c]
        self.assertEqual(len(one), 2)  # build, then the failing prepare; no run or summary

    def test_success_writes_empty_failure_list(self) -> None:
        with mock.patch.object(selection.subprocess, "call", return_value=0), \
             contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(selection.run(self.manifest, self.root, "control", None, self.out, 5), 0)
        self.assertEqual((self.out / "failed.txt").read_text(), "")

    def test_fandango_setup_failure_stops_before_targets(self) -> None:
        with mock.patch.object(selection.subprocess, "call", return_value=1) as call, \
             contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaisesRegex(ValueError, "fandango setup failed"):
                selection.run(self.manifest, self.root, "fandango", None, self.out, 5)
        self.assertEqual(call.call_count, 1)

    def test_manifest_validation(self) -> None:
        bad = {"schema": "other"}
        self.manifest.write_text(json.dumps(bad))
        with self.assertRaisesRegex(ValueError, "not a Parsarium selection"):
            selection.load(self.manifest)
        for broken, message in (({"id": "../x", "targets": [{}]}, "invalid selection ID"),
                                ({"id": "ok", "targets": []}, "lists no targets")):
            self.manifest.write_text(json.dumps({"schema": "parsarium-selection/1", **broken}))
            with self.assertRaisesRegex(ValueError, message):
                selection.load(self.manifest)

    def test_target_ids_cannot_escape_projects(self) -> None:
        data = json.loads(json.dumps({"schema": "parsarium-selection/1", "id": "sel", "commit": "c" * 8,
                                      "targets": [{"id": "png/../../etc", "format": "png", "ecosystem": ".."}]}))
        self.manifest.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, "invalid target ID"):
            selection.run(self.manifest, self.root, "control", None, self.out, 5, dry_run=True)


class DocumentationExampleTests(unittest.TestCase):
    """Commands shown to users must name targets that exist."""

    ROOT = Path(__file__).resolve().parents[1]

    def test_readme_examples_name_real_targets(self) -> None:
        import re
        pattern = re.compile(r"parsarium(?:\.py)? (?:show|run|build|replay|afl build|afl prepare|fandango generate|native prepare|report) "
                             r"([a-z0-9_]+) (c|cpp|go|java|javascript|python|rust|php) ([A-Za-z0-9_.-]+)")
        checked = 0
        docs = ["README.md", "src/parsarium/README.md", "projects/README.md", "fuzzing/README.md", "AGENTS.md"]
        docs += [str(p.relative_to(self.ROOT)) for p in sorted((self.ROOT / "website").glob("*/*/*.html"))]
        for doc in docs:
            for fmt, eco, slug in pattern.findall((self.ROOT / doc).read_text()):
                checked += 1
                self.assertTrue((self.ROOT / "projects" / fmt / eco / slug / "manifest.json").is_file(),
                                f"{doc} names a missing target: {fmt}/{eco}/{slug}")
        self.assertGreater(checked, 5)


if __name__ == "__main__":
    unittest.main()
