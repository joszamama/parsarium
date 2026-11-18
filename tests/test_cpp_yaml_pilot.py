"""C++ YAML pilot paths keep their pins, typed-tree oracle, metric and AFL++ feedback consistent."""

from hashlib import sha256
import gzip
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/cpp/yaml"
POPCON = ROOT / "data/curation/popcon-sourcemax-by_inst.gz"
_spec = importlib.util.spec_from_file_location("yaml_check_controls", ROOT / "controls/yaml/check_controls.py")
ORACLE = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ORACLE)


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def sourcemax(name: str) -> int:
    for line in gzip.decompress(POPCON.read_bytes()).decode("utf-8", "replace").splitlines():
        parts = line.split()
        if len(parts) > 2 and parts[1] == name:
            return int(parts[2])
    raise KeyError(name)


class CppYamlPilotTest(unittest.TestCase):
    def setUp(self):
        self.parsers = read(BASE / "parsers.json")
        self.records = {item["package"]: item for item in read(BASE / "verification.json")["third_party"]}

    def test_cell_counts_and_metric_order(self):
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(self.parsers))
        self.assertGreaterEqual(len(self.parsers), 1)
        # Debian-ranked paths first, then GitHub-star fallback paths ranked
        # separately (PROTOCOL.md); the two metrics are never mixed.
        star = [item for item in self.parsers if item["popularity"].get("selection") == "supplemental"]
        debian = [item for item in self.parsers if item not in star]
        self.assertEqual(self.parsers, debian + star)
        for group in (debian, star):
            values = [item["popularity"]["value"] for item in group]
            self.assertEqual(values, sorted(values, reverse=True))
        for parser in debian:
            popularity = parser["popularity"]
            self.assertEqual(popularity["source_sha256"], sha256(POPCON.read_bytes()).hexdigest())
            self.assertEqual(popularity["value"], sourcemax(popularity["debian_source"]))
        captured = {row["name"]: row for row in
                    read(BASE / "registry-snapshot.json").get("round_6_star_fallback", {})
                    .get("selected_star_paths", [])}
        for parser in star:
            popularity = parser["popularity"]
            self.assertEqual(popularity["metric"],
                             "GitHub stars (secondary, repository interest, not downloads)")
            self.assertGreaterEqual(popularity["value"], 100)
            row = captured[parser["name"]]
            self.assertEqual((row["stargazers_count"], row["response_sha256"], row["captured_at_utc"]),
                             (popularity["value"], popularity["response_sha256"],
                              popularity["captured_at_utc"]))
            self.assertFalse(row["fork"])

    def test_pins_oracle_receipts_and_feedback(self):
        for parser in self.parsers:
            with self.subTest(parser=parser["name"]):
                project = ROOT / parser["project"]
                slug = project.name
                manifest = read(project / "manifest.json")
                lock = read(project / "source-lock.json")[parser["name"]]
                dockerfile = (project / "Dockerfile").read_text()
                self.assertEqual((manifest["release"], lock["release"], parser["version"]),
                                 (parser["version"],) * 3)
                self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
                for pinned in (lock["source_sha256"], lock["source_url"], manifest["base_image"]):
                    self.assertIn(pinned, dockerfile)
                for key, control in (("expected_output", "catalog.yaml"),
                                     ("differential_expected_output", "order.yaml")):
                    self.assertEqual(manifest[key], {"tree": ORACLE.EXPECTED[control]})
                    self.assertEqual(parser[key], manifest[key])
                self.assertEqual(manifest["control_sha256"], ORACLE.CONTROLS["catalog.yaml"])
                self.assertEqual(manifest["differential_control_sha256"], ORACLE.CONTROLS["order.yaml"])
                self.assertEqual(read(project / "expected.json"), manifest["expected_output"])
                receipt = read(project / "verification.json")
                self.assertTrue(receipt["pass"])
                self.assertEqual(receipt["output"], manifest["expected_output"])
                self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
                record = self.records[parser["name"]]
                self.assertTrue(record["pass"])
                self.assertEqual(record["output"], manifest["expected_output"])
                overlay = ROOT / "fuzzing/afl-native/yaml/cpp" / slug
                overlay_receipt = read(overlay / "verification.json")
                self.assertEqual(overlay_receipt["base_project_receipt_sha256"],
                                 sha256((project / "verification.json").read_bytes()).hexdigest())
                diff = read(overlay / "differential.json")
                self.assertTrue(diff["pass"])
                self.assertEqual(diff["repeats_per_control"], 3)
                self.assertEqual(diff["overlay_receipt_sha256"],
                                 sha256((overlay / "verification.json").read_bytes()).hexdigest())
                self.assertGreater(diff["source_line_difference"], 0)
                self.assertGreater(diff["afl_tuple_difference"], 0)
                self.assertEqual(diff["second_control_output"], manifest["differential_expected_output"])

    def test_plain_scalars_are_typed_by_core_schema_patterns(self):
        # fkYAML resolves plain scalars itself; the other C++ libraries keep
        # them as text and their harnesses apply the core-schema patterns.
        self_typing = {"fkyaml"}
        for parser in self.parsers:
            harness = (ROOT / parser["project"] / "harness.cpp").read_text()
            self.assertIn("typing_note", parser)
            if parser["name"] in self_typing:
                self.assertNotIn("std::regex", harness)
                self.assertIn("is_integer()", harness)
                continue
            self.assertIn("[-+]?[0-9]+", harness)
            self.assertIn("true|True|TRUE|false|False|FALSE", harness)


if __name__ == "__main__":
    unittest.main()
