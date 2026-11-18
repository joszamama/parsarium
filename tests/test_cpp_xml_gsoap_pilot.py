"""The C++ gSOAP DOM path keeps its pins, namespace-aware outputs, weak metric label and own-engine feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/cpp/xml"
PACKAGE = "gsoap"
PROJECT = ROOT / "projects/xml/cpp/gsoap"
OVERLAY = ROOT / "fuzzing/afl-native/xml/cpp/gsoap"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def entry(name: str, items: list, key: str = "name") -> dict:
    found, = [item for item in items if item[key] == name]
    return found


class CppXmlGsoapPilotTest(unittest.TestCase):
    def test_pins_and_documented_dom_route(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")[PACKAGE]
        self.assertEqual((manifest["release"], lock["release"]), ("2.8.142", "2.8.142"))
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        for dockerfile in (PROJECT / "Dockerfile", OVERLAY / "Dockerfile"):
            text = dockerfile.read_text()
            for pinned in (lock["source_sha256"], lock["source_url"], manifest["base_image"]):
                self.assertIn(pinned, text)
        harness = (PROJECT / "harness.cpp").read_text()
        self.assertIn("in >> dom;", harness)
        self.assertIn("SOAP_C_UTFSTRING | SOAP_DOM_TREE", harness)
        build = (PROJECT / "build.sh").read_text()
        self.assertIn("soapcpp2 -CSL -I$src/import $src/import/dom.h", build)
        self.assertIn("-fno-sanitize=alignment", build)

    def test_shared_namespace_outputs(self):
        manifest = read(PROJECT / "manifest.json")
        tinyxml = read(ROOT / "projects/xml/cpp/tinyxml/manifest.json")
        self.assertEqual(manifest["expected_output"], tinyxml["expected_output"])
        self.assertEqual(manifest["differential_control"], "controls/xml/order-default-ns.xml")
        self.assertEqual(manifest["differential_expected_output"], tinyxml["differential_expected_output"])
        for control, digest in ((manifest["control"], manifest["control_sha256"]),
                                (manifest["differential_control"], manifest["differential_control_sha256"])):
            self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)

    def test_receipts_match_catalog(self):
        manifest = read(PROJECT / "manifest.json")
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
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)

    def test_metric_rank_and_leads(self):
        parsers = read(BASE / "parsers.json")
        parser = entry(PACKAGE, parsers)
        self.assertEqual(parser["popularity"]["dev_package_installs"], {"libgsoap-dev": 95})
        self.assertIn("Weak signal", parser["popularity"]["qualification"])
        values = [item["popularity"]["value"] for item in parsers]
        self.assertEqual(values, sorted(values, reverse=True))
        names = [item["name"] for item in parsers]
        self.assertEqual(names[names.index("libxml++"):], ["libxml++", PACKAGE, "cxxtools", "rapidxml"])
        snapshot = read(BASE / "registry-snapshot.json")
        self.assertEqual(entry("gSOAP", snapshot["candidates"], "library")["dev_installs"], 95)
        self.assertEqual(entry("gSOAP", read(BASE / "leads.json"))["status"], "resolved_verified_selected")
        self.assertEqual(read(BASE / "cell.json")["verified_third_party_count"], len(parsers))

    def test_feedback_is_stable_and_in_gsoap_sources(self):
        report = read(BASE / "afl-feedback.json")
        result = entry("xml/cpp/gsoap", report["results"], "project")
        overlay = read(OVERLAY / "verification.json")
        differential = read(OVERLAY / "differential.json")
        self.assertEqual(sha256((OVERLAY / "verification.json").read_bytes()).hexdigest(),
                         result["overlay_receipt_sha256"])
        self.assertEqual(sha256((OVERLAY / "differential.json").read_bytes()).hexdigest(),
                         result["differential_receipt_sha256"])
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertGreater(result["afl_tuple_difference"], 0)
        self.assertGreater(result["gsoap_engine_line_difference"], 0)
        files = set(differential["first_only_lines_by_file"]) | set(differential["second_only_lines_by_file"])
        self.assertLessEqual(files, {"stdsoap2.cpp", "stdsoap2.h", "dom.cpp"})


if __name__ == "__main__":
    unittest.main()
