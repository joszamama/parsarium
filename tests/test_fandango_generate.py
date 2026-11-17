"""Fandango generate command tests with a fake executable; no fuzzer or Docker runs.

Run: python3 -m unittest discover -s tests
"""

from contextlib import redirect_stderr, redirect_stdout
from hashlib import sha256
import importlib.util
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import textwrap
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import fandango_generate  # noqa: E402

_repo_cli_spec = importlib.util.spec_from_file_location("parsarium_repo_cli", ROOT / "parsarium.py")
repo_cli = importlib.util.module_from_spec(_repo_cli_spec)
_repo_cli_spec.loader.exec_module(repo_cli)


FAKE_SPEC = b"<start> ::= b'\\x89PNG'\n"
FAKE = textwrap.dedent('''\
    #!/usr/bin/env python3
    """Stand-in for fandango: logs argv/env and writes -n files into -d."""
    import json, os, sys
    from pathlib import Path
    mode = os.environ.get("FAKE_FANDANGO_MODE", "")
    if sys.argv[1:] == ["--version"]:
        print("fandango 1.2.0" if mode == "old" else "fandango 1.3.1")
        raise SystemExit(0)
    argv = sys.argv[1:]
    assert argv[0] == "fuzz", argv
    value = lambda flag: argv[argv.index(flag) + 1] if flag in argv else None
    Path(os.environ["FAKE_FANDANGO_LOG"]).write_text(json.dumps({
        "argv": argv, "cwd": os.getcwd(),
        "env": {key: os.environ.get(key) for key in
                ("FANDANGO_PATH", "FANBASE_REGISTRY", "PYTHONHASHSEED")}}))
    name = value("-F")
    if name and mode != "no-snapshot":
        home = Path(os.environ["FANDANGO_PATH"]) / name.split("-")[0]
        home.mkdir(parents=True)
        (home / f"{name}.fan").write_bytes(SPEC)
        (home / f"{name}.yml").write_text("version: '1.0'\\n")
    directory = Path(value("-d"))
    extension = value("-x") or "." + (name or "txt").split("-")[0]
    count = 0 if mode == "empty" else int(value("-n"))
    for index in range(count):
        payload = (Path(os.environ["FAKE_MP3_CONTROL"]).read_bytes()
                   if mode == "plain-mp3" else b"\\x89PNG" + bytes([index % 256]))
        (directory / f"out-{index}{extension}").write_bytes(payload)
    if mode == "symlink":
        (directory / "link").symlink_to("/etc/hosts")
    raise SystemExit(3 if mode == "fail" else 0)
    ''').replace("SPEC)", f"{FAKE_SPEC!r})")


class FandangoGenerateTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.tmp = Path(temp.name)
        self.fake = self.tmp / "bin" / "fandango"
        self.fake.parent.mkdir()
        self.fake.write_text(FAKE)
        self.fake.chmod(0o755)
        self.log = self.tmp / "fake-log.json"
        patcher = mock.patch.dict(os.environ, {"FAKE_FANDANGO_LOG": str(self.log)})
        patcher.start()
        self.addCleanup(patcher.stop)

    def run_cli(self, *argv: str, mode: str = "") -> tuple[int, str]:
        os.environ["FAKE_FANDANGO_MODE"] = mode
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                code = fandango_generate.main([*argv, "--fandango", str(self.fake)])
            except SystemExit as error:
                code = error.code
        return code, stdout.getvalue() + stderr.getvalue()

    def receipt(self, run: Path) -> dict:
        return json.loads((run / "fandango.json").read_text())

    def test_fanbase_command_receipt_and_snapshot(self):
        run = self.tmp / "png-run"
        code, output = self.run_cli("png", "c", "lodepng", str(run), "--fanbase", "png",
                                    "--count", "5", "--seed", "42")
        self.assertEqual(code, 0, output)
        logged = json.loads(self.log.read_text())
        self.assertEqual(logged["argv"], ["fuzz", "-F", "png", "-n", "5", "-d",
                                          str(run.resolve() / "generated"), "--random-seed", "42"])
        self.assertEqual(logged["env"]["FANDANGO_PATH"], str(run.resolve() / "fanbase-specs"))
        self.assertEqual(logged["env"]["PYTHONHASHSEED"], "42")
        self.assertIsNone(logged["env"]["FANBASE_REGISTRY"])
        receipt = self.receipt(run)
        self.assertEqual(receipt["project"], "png/c/lodepng")
        self.assertEqual(receipt["fandango"]["version"], "fandango 1.3.1")
        self.assertEqual(receipt["fandango"]["executable"], str(self.fake.resolve()))
        self.assertEqual(receipt["fandango"]["executable_sha256"],
                         sha256(self.fake.read_bytes()).hexdigest())
        self.assertEqual(receipt["command"][0], str(self.fake.resolve()))
        self.assertEqual(receipt["command"][1:], logged["argv"])
        self.assertEqual(receipt["project_receipt_sha256"], sha256(
            (ROOT / "projects/png/c/lodepng/verification.json").read_bytes()).hexdigest())
        self.assertEqual(receipt["seed"], 42)
        self.assertEqual(receipt["spec"]["sha256"], sha256(FAKE_SPEC).hexdigest())
        self.assertEqual(receipt["spec"]["snapshot"]["path"], "fanbase-specs/png/png.fan")
        self.assertFalse(receipt["spec"]["registry"]["pinned"])
        self.assertIsNone(receipt["spec"]["matches_registry_index"])
        self.assertEqual(receipt["output_count"], 5)
        first = receipt["outputs"][0]
        self.assertEqual(first, {"path": "out-0.png", "bytes": 5,
                                 "sha256": sha256(b"\x89PNG\x00").hexdigest()})
        self.assertEqual(receipt["problems"], [])
        self.assertEqual(receipt["bridges"], [])

    def test_default_fanbase_spec_needs_no_flag(self):
        run = self.tmp / "default-png"
        code, output = self.run_cli("png", "c", "lodepng", str(run), "--count", "1")
        self.assertEqual(code, 0, output)
        self.assertEqual(self.receipt(run)["spec"]["name"], "png")
        self.assertEqual(json.loads(self.log.read_text())["argv"][1:3], ["-F", "png"])

    def test_pilot_defaults_match_verified_fanbase_specs(self):
        for format_name, slug in (("json", "simplejson"), ("xml", "xmltodict")):
            with self.subTest(format=format_name):
                run = self.tmp / f"default-{format_name}"
                code, output = self.run_cli(format_name, "python", slug, str(run),
                                            "--count", "1")
                self.assertEqual(code, 0, output)
                self.assertEqual(self.receipt(run)["spec"]["name"], format_name)
                self.assertEqual(json.loads(self.log.read_text())["argv"][1:3],
                                 ["-F", format_name])
        self.assertIn("mp3", fandango_generate.FORMATS)
        self.assertNotIn("mp3", fandango_generate.FANBASE_FORMATS)
        self.assertEqual(fandango_generate.LOCAL_SPECS["mp3"], "mp3_plain.fan")

    def test_plain_mp3_default_uses_local_spec_and_checks_frames(self):
        control = ROOT / "controls/mp3/go-tone-44k-mono.mp3"
        run = self.tmp / "plain-mp3"
        with mock.patch.dict(os.environ, {"FAKE_MP3_CONTROL": str(control)}):
            code, output = self.run_cli("mp3", "go", "github_com_hajimehoshi_go_mp3",
                                        str(run), "--count", "1", "--seed", "7",
                                        mode="plain-mp3")
        self.assertEqual(code, 0, output)
        spec = ROOT / "fuzzing/fandango/specs/mp3_plain.fan"
        logged = json.loads(self.log.read_text())
        self.assertEqual(logged["argv"][1:5], ["-f", str(spec), "-x", ".mp3"])
        receipt = self.receipt(run)
        self.assertEqual(receipt["spec"]["sha256"], sha256(spec.read_bytes()).hexdigest())
        self.assertEqual(receipt["outputs"][0]["sha256"], sha256(control.read_bytes()).hexdigest())
        self.assertEqual(receipt["outputs"][0]["format_validation"]["frames"], 11)
        self.assertTrue(receipt["outputs"][0]["format_validation"]["pinned_go_and_rust_decode_checked"])
        self.assertEqual(receipt["problems"], [])

    def test_plain_mp3_bundled_route_rejects_other_valid_stream(self):
        control = ROOT / "controls/mp3/tone-44k-mono.mp3"
        run = self.tmp / "other-plain-mp3"
        with mock.patch.dict(os.environ, {"FAKE_MP3_CONTROL": str(control)}):
            code, output = self.run_cli("mp3", "go", "github_com_hajimehoshi_go_mp3",
                                        str(run), "--count", "1", mode="plain-mp3")
        self.assertEqual(code, 1, output)
        self.assertIn("differs from the six decoded samples", output)

    def test_plain_mp3_rejects_output_without_frames(self):
        run = self.tmp / "bad-plain-mp3"
        code, output = self.run_cli("mp3", "go", "github_com_hajimehoshi_go_mp3",
                                    str(run), "--count", "1")
        self.assertEqual(code, 1, output)
        self.assertIn("plain MP3 output is outside", output)
        self.assertEqual(len(self.receipt(run)["problems"]), 1)

    def test_standard_feedback_path_uses_control_receipt(self):
        run = self.tmp / "tkinter-png"
        code, output = self.run_cli("png", "python", "stdlib_tkinter_photoimage",
                                    str(run), "--count", "1")
        self.assertEqual(code, 0, output)
        receipt = self.receipt(run)
        self.assertEqual(receipt["release"], "CPython 3.13.1 with bundled Tk 8.6")
        self.assertEqual(receipt["project_receipt_sha256"], sha256(
            (ROOT / "projects/png/python/stdlib_tkinter_photoimage/control-verification.json")
            .read_bytes()).hexdigest())

    def test_default_local_mp4_spec_needs_no_flag(self):
        run = self.tmp / "default-mp4"
        code, output = self.run_cli("mp4", "cpp", "exiv2", str(run), "--count", "1")
        self.assertEqual(code, 0, output)
        spec = ROOT / "fuzzing/fandango/specs/mp4.fan"
        self.assertEqual(self.receipt(run)["spec"]["sha256"], sha256(spec.read_bytes()).hexdigest())
        self.assertEqual(json.loads(self.log.read_text())["argv"][1:4],
                         ["-f", str(spec), "-x"])

    def test_pinned_registry_checks_index_hash(self):
        registry = self.tmp / "fanbase"
        registry.mkdir()
        index = (f"schema: 2\nspecs:\n- format: png\n  kind: png\n"
                 f"  path: specs/png/png/png.fan\n  sha256: {{}}\n")
        (registry / "index.yml").write_text(index.format(sha256(FAKE_SPEC).hexdigest()))
        run = self.tmp / "pinned"
        code, output = self.run_cli("png", "c", "lodepng", str(run), "--fanbase", "png",
                                    "--fanbase-registry", str(registry), "--count", "1")
        self.assertEqual(code, 0, output)
        self.assertEqual(json.loads(self.log.read_text())["env"]["FANBASE_REGISTRY"],
                         str(registry.resolve()))
        spec = self.receipt(run)["spec"]
        self.assertTrue(spec["registry"]["pinned"])
        self.assertTrue(spec["matches_registry_index"])

        (registry / "index.yml").write_text(index.format("0" * 64))
        code, output = self.run_cli("png", "c", "lodepng", str(self.tmp / "mismatch"),
                                    "--fanbase", "png", "--fanbase-registry", str(registry))
        self.assertEqual(code, 1)
        self.assertIn("differs from the pinned registry index", output)

    def test_custom_spec_for_format_without_fanbase(self):
        spec = self.tmp / "mp4.fan"
        spec.write_text("<start> ::= b'ftyp'\n")
        run = self.tmp / "mp4-run"
        code, output = self.run_cli("mp4", "cpp", "exiv2", str(run), "--spec", str(spec),
                                    "--count", "3")
        self.assertEqual(code, 0, output)
        logged = json.loads(self.log.read_text())
        self.assertEqual(logged["argv"], ["fuzz", "-f", str(spec.resolve()), "-x", ".mp4",
                                          "-n", "3", "-d", str(run.resolve() / "generated")])
        self.assertIsNone(logged["env"]["FANDANGO_PATH"])
        self.assertIsNone(logged["env"]["PYTHONHASHSEED"])
        receipt = self.receipt(run)
        self.assertEqual(receipt["spec"]["sha256"], sha256(spec.read_bytes()).hexdigest())
        self.assertTrue(receipt["spec"]["unchanged_after_run"])
        self.assertEqual((run / "spec-mp4.fan").read_bytes(), spec.read_bytes())
        self.assertEqual([item["path"] for item in receipt["outputs"]],
                         ["out-0.mp4", "out-1.mp4", "out-2.mp4"])

    def test_rejects_invalid_requests_before_running(self):
        spec = self.tmp / "x.fan"
        spec.write_text("")
        cases = [
            (("mp4", "cpp", "exiv2", "--fanbase", "mp4"), "no mp4 spec"),
            (("png", "c", "lodepng", "--fanbase", "zip"), "must name a png spec"),
            (("png", "c", "lodepng", "--fanbase", "../png"), "must name a png spec"),
            (("png", "c", "lodepng", "--spec", str(self.tmp / "missing.fan")), "existing .fan"),
            (("png", "c", "lodepng", "--spec", str(spec), "--fanbase-registry", "x"),
             "applies only to --fanbase"),
            (("png", "c", "lodepng", "--fanbase", "png", "--count", "0"), "--count"),
            (("png", "c", "lodepng", "--fanbase", "png", "--seed", "-1"), "--seed"),
        ]
        for argv, message in cases:
            with self.subTest(argv=argv):
                code, output = self.run_cli(*argv[:3], str(self.tmp / "never"), *argv[3:])
                self.assertEqual(code, 2)
                self.assertIn(message, output)
        self.assertFalse((self.tmp / "never").exists())
        self.assertFalse(self.log.exists())

    def test_rejects_unknown_project(self):
        code, output = self.run_cli("png", "c", "../../mp4/cpp/exiv2", str(self.tmp / "run"),
                                    "--fanbase", "png")
        self.assertEqual(code, 2)
        self.assertIn("slug must be", output)
        with self.assertRaisesRegex(ValueError, "unknown project"):
            self.run_cli("png", "cpp", "libpng", str(self.tmp / "run"), "--fanbase", "png")

    def test_output_directory_rules(self):
        busy = self.tmp / "busy"
        busy.mkdir()
        (busy / "keep").write_text("x")
        for path in (busy, ROOT / "data" / "fandango-test", ROOT / "runs", ROOT):
            with self.subTest(path=path), self.assertRaises(ValueError):
                self.run_cli("png", "c", "lodepng", str(path), "--fanbase", "png")
        self.assertFalse((ROOT / "data" / "fandango-test").exists())
        self.assertEqual(fandango_generate.output_directory(ROOT / "runs" / "new-x"),
                         ROOT / "runs" / "new-x")

    def test_old_version_is_refused(self):
        with self.assertRaisesRegex(RuntimeError, "older than 1.3"):
            self.run_cli("png", "c", "lodepng", str(self.tmp / "run"), "--fanbase", "png",
                         mode="old")
        self.assertFalse(self.log.exists())

    def test_failed_generation_records_problems_and_skips_bridges(self):
        for mode, message in (("fail", "did not exit cleanly"), ("empty", "no files"),
                              ("symlink", "symlinks"), ("no-snapshot", "installed png.fan")):
            run = self.tmp / f"run-{mode}"
            with self.subTest(mode=mode), mock.patch.object(
                    fandango_generate.subprocess, "call") as call:
                code, output = self.run_cli("png", "c", "lodepng", str(run), "--fanbase", "png",
                                            "--count", "2", "--replay", "--prepare-afl",
                                            mode=mode)
                self.assertEqual(code, 1)
                self.assertIn(message, output)
                call.assert_not_called()
                self.assertTrue(any(message in problem
                                    for problem in self.receipt(run)["problems"]))

    def test_bridges_use_existing_replay_and_afl_prepare(self):
        run = self.tmp / "bridged"
        with mock.patch.object(fandango_generate.subprocess, "call", return_value=0) as call:
            code, output = self.run_cli("png", "c", "lodepng", str(run), "--fanbase", "png",
                                        "--count", "2", "--seed", "7", "--replay", "--prepare-afl")
        self.assertEqual(code, 0, output)
        replay, prepare = [entry.args[0] for entry in call.call_args_list]
        generated = str(run.resolve() / "generated")
        receipt = self.receipt(run)
        self.assertEqual(replay[1:8], [str(ROOT / "scripts/replay_corpus.py"), "png", "c",
                                       "lodepng", generated, str(run.resolve() / "replay"),
                                       "--generator"])
        self.assertEqual(replay[replay.index("--spec") + 1], "png")
        self.assertEqual(replay[replay.index("--spec-sha256") + 1], sha256(FAKE_SPEC).hexdigest())
        self.assertEqual(replay[replay.index("--generator-version") + 1], "fandango 1.3.1")
        self.assertIn("--random-seed 7",
                      replay[replay.index("--generator-command") + 1])
        self.assertEqual(prepare[1:], [str(ROOT / "scripts/prepare_afl_run.py"), "png", "c",
                                       "lodepng", str(run.resolve() / "afl"),
                                       "--seed-dir", generated])
        self.assertNotIn("run_prepared_afl.py", " ".join(map(str, prepare)))
        self.assertEqual([item["step"] for item in receipt["bridges"]], ["replay", "afl_prepare"])
        self.assertIn("prepared, not started", output)

    def test_parsarium_cli_routes_to_generator(self):
        run = self.tmp / "via-cli"
        argv = ["parsarium.py", "fandango", "generate", "png", "c", "lodepng", str(run),
                "--fanbase", "png", "--count", "1", "--fandango", str(self.fake)]
        os.environ["FAKE_FANDANGO_MODE"] = ""
        with mock.patch.object(sys, "argv", argv), redirect_stdout(io.StringIO()):
            self.assertEqual(repo_cli.main(), 0)
        self.assertEqual(self.receipt(run)["output_count"], 1)

    def test_parsarium_cli_routes_to_setup(self):
        with mock.patch.object(sys, "argv", ["parsarium.py", "fandango", "setup"]), \
             mock.patch.object(fandango_generate, "setup", return_value=0) as setup:
            self.assertEqual(repo_cli.main(), 0)
            setup.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()
