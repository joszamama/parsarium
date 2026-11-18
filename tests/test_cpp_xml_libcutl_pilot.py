"""The C++ libcutl path keeps its pins, Expat-family label, fixed salt, weak metric and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/cpp/xml"
PACKAGE = "libcutl"
PROJECT = ROOT / "projects/xml/cpp/libcutl"
OVERLAY = ROOT / "fuzzing/afl-native/xml/cpp/libcutl"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def entry(name: str, items: list, key: str = "name") -> dict:
    found, = [item for item in items if item[key] == name]
    return found


class CppXmlLibcutlPilotTest(unittest.TestCase):
    def test_pins_agree_with_expat_cell(self):
        manifest = read(PROJECT / "manifest.json")
        locks = read(PROJECT / "source-lock.json")
        self.assertEqual(manifest["release"], locks[PACKAGE]["release"])
        self.assertEqual(manifest["source_sha256"], locks[PACKAGE]["source_sha256"])
        self.assertEqual(locks["expat"], read(ROOT / "projects/xml/c/expat/source-lock.json")["expat"])
        self.assertEqual(manifest["underlying_source_sha256"], locks["expat"]["source_sha256"])
        for dockerfile in (PROJECT / "Dockerfile", OVERLAY / "Dockerfile"):
            text = dockerfile.read_text()
            for pinned in (locks[PACKAGE]["source_sha256"], locks[PACKAGE]["source_url"],
                           locks["expat"]["source_sha256"], locks["expat"]["source_url"], manifest["base_image"]):
                self.assertIn(pinned, text)
        harness = (PROJECT / "harness.cpp").read_text()
        self.assertIn("parser::receive_namespace_decls", harness)
        self.assertIn('extern "C" void arc4random_buf', harness)
        self.assertIn("#define LIBCUTL_EXTERNAL_EXPAT 1", (PROJECT / "build.sh").read_text())

    def test_receipts_match_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        tinyxml = read(ROOT / "projects/xml/cpp/tinyxml/manifest.json")
        self.assertEqual(manifest["expected_output"], tinyxml["expected_output"])
        self.assertEqual(manifest["differential_expected_output"], tinyxml["differential_expected_output"])
        receipt = read(PROJECT / "verification.json")
        parser = entry(PACKAGE, read(BASE / "parsers.json"))
        record = entry(PACKAGE, read(BASE / "verification.json")["third_party"], "package")
        differential = read(OVERLAY / "differential.json")
        self.assertTrue(receipt["pass"] and record["pass"] and differential["pass"])
        for output in (receipt["output"], parser["expected_output"], record["output"]):
            self.assertEqual(output, manifest["expected_output"])
        for output in (parser["differential_expected_output"], record["second_valid_output"],
                       differential["second_control_output"]):
            self.assertEqual(output, manifest["differential_expected_output"])
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        self.assertIn("Expat family", parser["family"])

    def test_metric_rank_and_leads(self):
        parsers = read(BASE / "parsers.json")
        parser = entry(PACKAGE, parsers)
        self.assertEqual(parser["popularity"]["dev_package_installs"], {"libcutl-dev": 3})
        self.assertIn("Very weak signal", parser["popularity"]["qualification"])
        values = [item["popularity"]["value"] for item in parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        self.assertEqual(parsers[-1]["name"], PACKAGE)
        self.assertEqual(len(parsers), 10)
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(cell["ceiling"], len(parsers))
        leads = read(BASE / "leads.json")
        self.assertEqual(entry(PACKAGE, leads)["status"], "resolved_verified_selected")
        for name in ("Arabica", "ACEXML"):
            self.assertEqual(entry(name, leads)["status"], "unresolved_below_ceiling")
            self.assertLess(sum(entry(name, leads)["popcon_dev_package"].values()), parser["popularity"]["value"])

    def test_feedback_is_stable_and_differential(self):
        result = entry("xml/cpp/libcutl", read(BASE / "afl-feedback.json")["results"], "project")
        overlay = read(OVERLAY / "verification.json")
        self.assertEqual(sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
                         result["overlay_receipt_sha256"])
        self.assertEqual(sha256((OVERLAY / "differential.json").read_bytes()).hexdigest(),
                         result["differential_receipt_sha256"])
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertGreater(result["afl_tuple_difference"], 0)
        self.assertGreater(result["underlying_expat_line_difference"], 0)


if __name__ == "__main__":
    unittest.main()
