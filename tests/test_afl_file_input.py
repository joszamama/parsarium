"""Regression checks for file-backed AFL++ plans.

Run: python3 -m unittest tests.test_afl_file_input
"""

import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from prepare_afl_run import commands_for, uses_afl_file_input  # noqa: E402


class AFLFileInputTest(unittest.TestCase):
    def command(self, manifest: dict) -> tuple[list[str], list[str]]:
        receipt = {"afl_map_size": 65536, "image_id": "sha256:" + "1" * 64}
        return commands_for(manifest, receipt, Path("/seeds"), Path("/results"),
                            1000, "parsarium-test")

    def test_native_c_and_cpp_targets_get_file_argument_by_default(self):
        for ecosystem in ("c", "cpp"):
            with self.subTest(ecosystem=ecosystem):
                manifest = {"ecosystem": ecosystem, "platform": "linux/arm64"}
                command, resume = self.command(manifest)
                self.assertEqual(command[-3:], ["--", "/work/fuzzer", "@@"])
                self.assertEqual(resume[-3:], ["--", "/work/fuzzer", "@@"])

    def test_explicit_file_input_and_stdin_override(self):
        manifest = {"ecosystem": "c", "platform": "linux/arm64",
                    "afl_entrypoint": "/work/custom", "afl_file_input": True}
        self.assertEqual(self.command(manifest)[0][-3:], ["--", "/work/custom", "@@"])
        manifest["afl_file_input"] = False
        self.assertEqual(self.command(manifest)[0][-2:], ["--", "/work/custom"])

    def test_every_current_native_manifest_uses_file_input(self):
        paths = sorted((ROOT / "projects").glob("*/*/*/manifest.json"))
        native = [json.loads(path.read_text()) for path in paths
                  if path.parent.parent.name in {"c", "cpp"}]
        self.assertTrue(native)
        for manifest in native:
            with self.subTest(package=manifest.get("package"), ecosystem=manifest["ecosystem"]):
                self.assertTrue(uses_afl_file_input(manifest))
                command, resume = self.command(manifest)
                entrypoint = manifest.get("afl_entrypoint", "/work/fuzzer")
                self.assertEqual(command[-3:], ["--", entrypoint, "@@"])
                self.assertEqual(resume[-3:], ["--", entrypoint, "@@"])

    def test_managed_proxy_remains_file_backed(self):
        manifest = {"ecosystem": "python", "platform": "linux/arm64"}
        self.assertEqual(self.command(manifest)[0][-3:], ["--", "/work/afl_proxy", "@@"])

    def test_rust_afl_targets_consume_shared_memory_or_stdin(self):
        paths = sorted((ROOT / "projects").glob("*/rust/*/manifest.json"))
        self.assertTrue(paths)
        for path in paths:
            manifest = json.loads(path.read_text())
            with self.subTest(project=str(path.parent.relative_to(ROOT / "projects"))):
                command, resume = self.command(manifest)
                self.assertEqual(command[-2:], ["--", "/work/afl_fuzzer"])
                self.assertEqual(resume[-2:], ["--", "/work/afl_fuzzer"])


if __name__ == "__main__":
    unittest.main()
