"""The C gdome2 path keeps its Debian pins, namespace-aware expat oracle, libxml2 family and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/c/xml"
PACKAGE = "gdome2"
PROJECT = ROOT / "projects/xml/c/gdome2"
OVERLAY = ROOT / "fuzzing/afl-native/xml/c/gdome2"

def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def entry(name: str, items: list, key: str = "name") -> dict:
    found, = [item for item in items if item[key] == name]
    return found


class CXmlGdome2PilotTest(unittest.TestCase):
    def test_pins_agree(self):
        manifest = read(PROJECT / "manifest.json")
        locks = read(PROJECT / "source-lock.json")
        lock = locks[PACKAGE]
        self.assertEqual((manifest["release"], lock["release"]), ("0.8.1+debian-10", "0.8.1+debian-10"))
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        self.assertEqual(manifest["underlying_source_sha256"], locks["libxml2"]["source_sha256"])
        self.assertEqual(locks["libxml2"]["source_sha256"], read(ROOT / "projects/xml/c/libxml2/manifest.json")["source_sha256"])
        for dockerfile in (PROJECT / "Dockerfile", OVERLAY / "Dockerfile"):
            text = dockerfile.read_text()
            for pinned in (lock["source_sha256"], lock["source_url"], lock["debian_tarball_sha256"],
                           locks["libxml2"]["source_sha256"], manifest["base_image"]):
                self.assertIn(pinned, text)
        self.assertIn("gdome_di_createDocFromMemory(impl, copy, GDOME_LOAD_PARSING", (PROJECT / "harness.c").read_text())

    def test_expected_outputs_are_the_shared_oracle(self):
        manifest = read(PROJECT / "manifest.json")
        self.assertIs(manifest["namespace_resolution"], True)
        expat = read(ROOT / "projects/xml/c/expat/manifest.json")
        self.assertEqual(manifest["expected_output"], expat["expected_output"])
        self.assertEqual(manifest["differential_expected_output"], expat["differential_expected_output"])
        for control, digest in ((manifest["control"], manifest["control_sha256"]),
                                (manifest["differential_control"], manifest["differential_control_sha256"])):
            self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)

    def test_receipts_match_catalog(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        parser = entry(PACKAGE, read(BASE / "parsers.json"))
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        self.assertEqual(parser["expected_output"], manifest["expected_output"])
        self.assertEqual(parser["differential_expected_output"], manifest["differential_expected_output"])
        self.assertEqual(parser["version"], manifest["release"])
        self.assertIn("libxml2", parser["shared_families"])
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        overlay = read(OVERLAY / "verification.json")
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        result = entry("xml/c/gdome2", read(BASE / "afl-feedback.json")["results"], "project")
        self.assertTrue(result["pass"] and result["repeated_controls_identical"])
        self.assertGreater(result["afl_tuple_difference"], 0)
        self.assertEqual(result["second_control_output"], manifest["differential_expected_output"])
        self.assertEqual(result["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())

    def test_metric_rank_and_round4_leads(self):
        parsers = read(BASE / "parsers.json")
        parser = entry(PACKAGE, parsers)
        snapshot = read(BASE / "registry-snapshot.json")
        candidate = snapshot["c_candidates"][PACKAGE]
        self.assertEqual(parser["metric"]["value"], candidate["primary_installed"])
        self.assertEqual(parser["metric"]["value"], 518)
        values = [item["metric"]["value"] for item in parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        names = [item["name"] for item in parsers]
        self.assertEqual(names[names.index("mxml") + 1], PACKAGE)
        leads = read(BASE / "leads.json")["leads"]
        self.assertEqual(entry(PACKAGE, leads)["status"], "selected")
        self.assertEqual(entry("neon", leads)["status"], "unresolved_no_primary_metric")
        self.assertEqual(entry("apr-util (apr_xml)", leads)["status"], "unresolved_no_primary_metric")
        self.assertEqual(entry("libxmltok (expat 1.2)", leads)["status"], "excluded")
        search = snapshot["debian_binary_search"]
        continuation = search["round_4_continuation"]
        self.assertEqual(search["recorded"] + continuation["recorded"], search["total"])
        self.assertEqual(sum(continuation["classification_counts"].values()), continuation["recorded"])
        self.assertEqual(continuation["hits"][0]["position"], 101)
        self.assertEqual(snapshot["round_4_targeted_binary_lookups"]["snapshot_sha256"], search["snapshot_sha256"])


if __name__ == "__main__":
    unittest.main()
