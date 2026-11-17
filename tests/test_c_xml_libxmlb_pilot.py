"""The C libxmlb path keeps its pins, raw-name expat oracle, metric and allowlisted feedback consistent."""

from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/c/xml"
PACKAGE = "libxmlb"
PROJECT = ROOT / "projects/xml/c/libxmlb"
OVERLAY = ROOT / "fuzzing/afl-native/xml/c/libxmlb"

_spec = importlib.util.spec_from_file_location("libxmlb_oracle", PROJECT / "oracle.py")
oracle = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(oracle)


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def entry(name: str, items: list, key: str = "name") -> dict:
    found, = [item for item in items if item[key] == name]
    return found


class CXmlLibxmlbPilotTest(unittest.TestCase):
    def test_pins_agree(self):
        manifest = read(PROJECT / "manifest.json")
        locks = read(PROJECT / "source-lock.json")
        lock, glib = locks[PACKAGE], locks["glib"]
        self.assertEqual((manifest["release"], lock["release"], glib["release"]), ("0.3.30", "0.3.30", "2.88.4"))
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        self.assertEqual(manifest["underlying_source_sha256"], glib["source_sha256"])
        for dockerfile in (PROJECT / "Dockerfile", OVERLAY / "Dockerfile"):
            text = dockerfile.read_text()
            for pinned in (lock["source_sha256"], lock["source_url"], glib["source_sha256"],
                           glib["source_url"], manifest["base_image"]):
                self.assertIn(pinned, text)
        self.assertEqual((PROJECT / "afl-allowlist.txt").read_text().split(),
                         ["src:glib/glib/gmarkup.c", "src:source/src/xb-*.c"])
        build = (PROJECT / "build.sh").read_text()
        self.assertIn("AFL_LLVM_ALLOWLIST=/work/afl-allowlist.txt", build)
        self.assertIn("__sanitizer_cov_trace_pc_guard_init", build)
        self.assertIn("xb_builder_source_load_xml", (PROJECT / "harness.c").read_text())

    def test_raw_name_oracle_matches_both_controls(self):
        manifest = read(PROJECT / "manifest.json")
        self.assertIs(manifest["namespace_resolution"], False)
        for control, digest, expected in (
                (manifest["control"], manifest["control_sha256"], manifest["expected_output"]),
                (manifest["differential_control"], manifest["differential_control_sha256"],
                 manifest["differential_expected_output"])):
            data = (ROOT / control).read_bytes()
            self.assertEqual(sha256(data).hexdigest(), digest)
            self.assertEqual(oracle.summarize(data), expected, control)

    def test_receipts_match_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser = entry(PACKAGE, read(BASE / "parsers.json"))
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        self.assertEqual(parser["differential_expected_output"], manifest["differential_expected_output"])
        self.assertEqual(parser["version"], manifest["release"])
        self.assertGreater(receipt["parser_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        self.assertEqual(receipt["underlying_source_files"], 1)
        overlay = read(OVERLAY / "verification.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        result = entry("xml/c/libxmlb", read(BASE / "afl-feedback.json")["results"], "project")
        self.assertTrue(result["pass"] and result["repeated_controls_identical"])
        self.assertGreater(result["afl_tuple_difference"], 0)
        self.assertEqual(result["second_control_output"], manifest["differential_expected_output"])
        self.assertEqual(result["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())

    def test_metric_and_family(self):
        parser = entry(PACKAGE, read(BASE / "parsers.json"))
        snapshot = read(BASE / "registry-snapshot.json")
        candidate = snapshot["c_candidates"][PACKAGE]
        self.assertEqual(parser["metric"]["value"], candidate["primary_installed"])
        self.assertEqual(candidate["debian_binary_packages"]["libxmlb2"]["installed"], 130663)
        self.assertIn("GLib GMarkup", parser["shared_families"])
        hit = entry(PACKAGE, snapshot["debian_source_search"]["hits"])
        self.assertEqual(hit["classification"], "c_xml_parser_library")
        self.assertEqual(entry(PACKAGE, read(BASE / "leads.json")["leads"])["status"], "selected")
        glib = entry("glib2.0 (GMarkup)", read(BASE / "leads.json")["leads"])
        self.assertEqual(glib["status"], "unresolved_no_primary_metric")
        self.assertIsNone(glib["popcon_installed"])
        names = [item["name"] for item in read(BASE / "parsers.json")]
        self.assertEqual(names.index(PACKAGE), names.index("libxml2") + 1)


if __name__ == "__main__":
    unittest.main()
