"""`afl prepare --fandango` / `native prepare --fandango` seed generation and provenance.

A fake Fandango executable and a faked `docker image inspect` keep these tests
offline: no fuzzer, generator or container runs.

Run: python3 -m unittest tests.test_fandango_seeds
"""

from contextlib import redirect_stderr, redirect_stdout
from hashlib import sha256
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import fandango_generate  # noqa: E402
import fandango_seeds  # noqa: E402
import prepare_afl_run  # noqa: E402
import prepare_native_run  # noqa: E402
import summarize_afl_run  # noqa: E402
from test_fandango_generate import FAKE  # noqa: E402

_repo_cli_spec = importlib.util.spec_from_file_location("parsarium_repo_cli_seeds", ROOT / "parsarium.py")
repo_cli = importlib.util.module_from_spec(_repo_cli_spec)
_repo_cli_spec.loader.exec_module(repo_cli)

TARGET = ("toml", "go", "github_com_pelletier_go_toml_v2")
PROJECT = "/".join(TARGET)
SPEC = ROOT / "fuzzing/fandango/specs/toml.fan"
REAL_RUN = subprocess.run


def manifest() -> dict:
    return json.loads((ROOT / "projects" / PROJECT / "manifest.json").read_text())


def fake_docker(afl_image: str, base_image: str, platform: str):
    """Answer docker image inspect with the receipt image IDs; run anything else."""
    def run(command, *args, **kwargs):
        if list(command[:3]) == ["docker", "image", "inspect"]:
            image = afl_image if command[3].startswith("parsarium-afl/") else base_image
            stdout = f"{image} {platform}" if "{{.Os}}" in command[-1] else image
            return subprocess.CompletedProcess(command, 0, stdout=stdout + "\n", stderr="")
        return REAL_RUN(command, *args, **kwargs)
    return run


class FandangoSeedTest(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.tmp = Path(temp.name).resolve()
        self.fake = self.tmp / "bin" / "fandango"
        self.fake.parent.mkdir()
        self.fake.write_text(FAKE)
        self.fake.chmod(0o755)
        environment = mock.patch.dict(os.environ, {"FAKE_FANDANGO_LOG": str(self.tmp / "log.json"),
                                                   "FAKE_FANDANGO_MODE": ""})
        environment.start()
        self.addCleanup(environment.stop)
        executable = mock.patch.object(fandango_generate, "fandango_executable",
                                       return_value=self.fake.resolve())
        executable.start()
        self.addCleanup(executable.stop)
        afl = json.loads((ROOT / "fuzzing/afl-native" / PROJECT / "verification.json").read_text())
        base = json.loads((ROOT / "projects" / PROJECT / "verification.json").read_text())
        docker = mock.patch.object(subprocess, "run",
                                   side_effect=fake_docker(afl["image_id"], base["image_id"],
                                                           manifest()["platform"]))
        docker.start()
        self.addCleanup(docker.stop)

    def prepare(self, module, *argv: str) -> tuple[int, str]:
        stdout, stderr = io.StringIO(), io.StringIO()
        with mock.patch.object(sys, "argv", [module.__file__, *argv]), \
             redirect_stdout(stdout), redirect_stderr(stderr):
            try:
                module.main()
                code = 0
            except SystemExit as error:
                code = error.code
        return code, stdout.getvalue() + stderr.getvalue()

    def check_provenance(self, run: Path, plan: dict, count: int, random_seed: int) -> None:
        record = plan["seed_generation"]
        self.assertEqual(record["generator"], "Fandango")
        self.assertEqual(record["generator_version"], "fandango 1.3.1")
        self.assertEqual(record["spec_kind"], "file")
        self.assertEqual(record["spec"], "fuzzing/fandango/specs/toml.fan")
        self.assertEqual(record["spec_sha256"], sha256(SPEC.read_bytes()).hexdigest())
        self.assertEqual(record["random_seed"], random_seed)
        self.assertEqual((record["requested_count"], record["output_count"],
                          record["unique_outputs"]), (count, count, count))
        self.assertEqual(record["receipt"], "fandango/fandango.json")
        self.assertEqual(record["receipt_sha256"],
                         sha256((run / "fandango/fandango.json").read_bytes()).hexdigest())
        command = record["generator_command"]
        self.assertEqual(command[1:5], ["fuzz", "-f", "$PARSARIUM_HOME/fuzzing/fandango/specs/toml.fan",
                                        "-x"])
        self.assertEqual(command[command.index("-d") + 1], "$RUN_DIR/fandango/generated")
        self.assertEqual(command[command.index("--random-seed") + 1], str(random_seed))
        self.assertNotIn(str(ROOT), json.dumps(record))
        self.assertNotIn(str(run), json.dumps(record))
        origins = [item["origin"] for item in plan["seed_sources"]]
        self.assertEqual(origins, ["control"] + ["fandango"] * count)
        self.assertEqual(plan["seed_sources"][0]["sha256"], manifest()["control_sha256"])
        self.assertEqual(plan["unique_seeds"], count + 1)

    def test_afl_prepare_generates_seeds_and_records_provenance(self):
        run = self.tmp / "afl"
        code, output = self.prepare(prepare_afl_run, *TARGET, str(run),
                                    "--fandango", "3", "--fandango-seed", "5")
        self.assertEqual(code, 0, output)
        self.assertIn("Prepared 4 seeds", output)
        self.assertNotIn("only seed is the control", output)
        plan = json.loads((run / "plan.json").read_text())
        self.check_provenance(run, plan, 3, 5)
        self.assertEqual(sorted(path.name for path in (run / "seeds").iterdir()),
                         sorted(item["sha256"] for item in plan["seed_sources"]))
        argv = json.loads((self.tmp / "log.json").read_text())["argv"]
        self.assertEqual(argv[:3], ["fuzz", "-f", str(SPEC)])
        self.assertEqual(argv[argv.index("-n") + 1], "3")

    def test_afl_prepare_default_keeps_control_only_plan(self):
        run = self.tmp / "control-only"
        code, output = self.prepare(prepare_afl_run, *TARGET, str(run))
        self.assertEqual(code, 0, output)
        self.assertIn("only seed is the control", output)
        plan = json.loads((run / "plan.json").read_text())
        self.assertNotIn("seed_generation", plan)
        self.assertEqual(plan["unique_seeds"], 1)
        self.assertEqual(plan["seed_sources"][0]["origin"], "control")
        self.assertFalse((run / "fandango").exists())

    def test_native_prepare_generates_seeds_and_records_provenance(self):
        run = self.tmp / "native"
        code, output = self.prepare(prepare_native_run, *TARGET, str(run),
                                    "--fandango", "2", "--duration-seconds", "5")
        self.assertEqual(code, 0, output)
        plan = json.loads((run / "plan.json").read_text())
        self.check_provenance(run, plan, 2, fandango_seeds.DEFAULT_RANDOM_SEED)
        self.assertEqual(len(plan["corpus_files"]), 3)
        self.assertTrue(all(path.read_text().startswith("go test fuzz v1\n")
                            for path in (run / "corpus").iterdir()))

    def test_existing_receipt_is_checked_against_its_files(self):
        generated = self.tmp / "generated-run"
        with redirect_stdout(io.StringIO()):
            self.assertEqual(fandango_generate.main([*TARGET, str(generated), "--count", "2",
                                                     "--seed", "9"]), 0)
        run = self.tmp / "from-receipt"
        code, output = self.prepare(prepare_afl_run, *TARGET, str(run), "--fandango-receipt",
                                    str(generated / "fandango.json"))
        self.assertEqual(code, 0, output)
        record = json.loads((run / "plan.json").read_text())["seed_generation"]
        self.assertEqual(record["random_seed"], 9)
        self.assertNotIn("receipt_sha256", record)
        self.assertTrue(record["receipt"].endswith("generated-run/fandango.json"))
        first = sorted((generated / "generated").iterdir())[0]
        first.write_bytes(b"changed")
        code, output = self.prepare(prepare_afl_run, *TARGET, str(self.tmp / "changed"),
                                    "--fandango-receipt", str(generated / "fandango.json"))
        self.assertEqual(code, 2)
        self.assertIn("changed after generation", output)

    def test_receipt_for_another_project_is_refused(self):
        generated = self.tmp / "other"
        with redirect_stdout(io.StringIO()):
            self.assertEqual(fandango_generate.main(["toml", "go", "github_com_burntsushi_toml",
                                                     str(generated), "--count", "1"]), 0)
        code, output = self.prepare(prepare_afl_run, *TARGET, str(self.tmp / "mismatch"),
                                    "--fandango-receipt", str(generated / "fandango.json"))
        self.assertEqual(code, 2)
        self.assertIn("not " + PROJECT, output)

    def test_failed_generation_stops_preparation(self):
        os.environ["FAKE_FANDANGO_MODE"] = "fail"
        run = self.tmp / "failed"
        code, output = self.prepare(prepare_afl_run, *TARGET, str(run), "--fandango", "2")
        self.assertEqual(code, 2)
        self.assertIn("Fandango seed generation failed", output)
        self.assertIn("Fandango did not exit cleanly", output)
        self.assertFalse((run / "plan.json").exists())

    def test_invalid_counts_and_conflicting_sources(self):
        for argv in (("--fandango", "0"), ("--fandango", "10001"),
                     ("--fandango", "2", "--fandango-seed", "-1"),
                     ("--fandango", "2", "--fandango-receipt", str(SPEC))):
            with self.subTest(argv=argv):
                code, _ = self.prepare(prepare_afl_run, *TARGET, str(self.tmp / "bad"), *argv)
                self.assertEqual(code, 2)
                self.assertFalse((self.tmp / "bad").exists())


class ForwardingTest(unittest.TestCase):
    def test_parsarium_cli_forwards_fandango_options(self):
        for action, script in (("afl", "prepare_afl_run.py"), ("native", "prepare_native_run.py")):
            with self.subTest(action=action), \
                 mock.patch.object(sys, "argv", ["parsarium.py", action, "prepare", *TARGET, "runs/x",
                                                 "--fandango", "100", "--fandango-seed", "7"]), \
                 mock.patch.object(repo_cli, "execute", return_value=0) as execute:
                self.assertEqual(repo_cli.main(), 0)
                arguments = execute.call_args.args
                self.assertEqual(arguments[0], script)
                index = arguments.index("--fandango")
                self.assertEqual(arguments[index:index + 4],
                                 ("--fandango", "100", "--fandango-seed", "7"))

    def test_parsarium_cli_without_fandango_passes_no_option(self):
        with mock.patch.object(sys, "argv", ["parsarium.py", "afl", "prepare", *TARGET, "runs/x"]), \
             mock.patch.object(repo_cli, "execute", return_value=0) as execute:
            self.assertEqual(repo_cli.main(), 0)
        self.assertNotIn("--fandango", execute.call_args.args)


class SummaryTest(unittest.TestCase):
    def test_summary_counts_imported_seeds_and_copies_provenance(self):
        with tempfile.TemporaryDirectory() as temporary:
            run = Path(temporary)
            provenance = {"generator": "Fandango", "spec": "fuzzing/fandango/specs/toml.fan"}
            (run / "plan.json").write_text(json.dumps({
                "project": PROJECT, "image_id": "sha256:" + "0" * 64, "unique_seeds": 3,
                "seed_generation": provenance}))
            queue = run / "afl-out/default/queue"
            queue.mkdir(parents=True)
            (run / "afl-out/default/fuzzer_stats").write_text("execs_done : 10\ncorpus_count : 4\n")
            for name in ("id:000000,time:0,execs:0,orig:a", "id:000001,time:0,execs:0,orig:b",
                         "id:000002,time:0,execs:0,orig:c", "id:000003,src:000001,time:5,execs:9,op:havoc"):
                (queue / name).write_bytes(b"x")
            with mock.patch.object(sys, "argv", ["summarize_afl_run.py", str(run)]), \
                 redirect_stdout(io.StringIO()) as output:
                summarize_afl_run.main()
            report = json.loads((run / "afl-summary.json").read_text())
        self.assertEqual(report["unique_seeds"], 3)
        self.assertEqual(report["seed_generation"], provenance)
        self.assertEqual(report["instances"][0]["initial_queue_entries"], 3)
        self.assertEqual(len(report["instances"][0]["queue"]), 4)
        self.assertIn("seeds=3 paths=4", output.getvalue())


if __name__ == "__main__":
    unittest.main()
