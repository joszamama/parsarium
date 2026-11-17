"""Pilot format cells remain visible without entering active aggregate gates."""

import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import build_matrix  # noqa: E402
import format_registry  # noqa: E402
import validate_catalog  # noqa: E402

_repo_cli_spec = importlib.util.spec_from_file_location("parsarium_repo_cli", ROOT / "parsarium.py")
parsarium = importlib.util.module_from_spec(_repo_cli_spec)
_repo_cli_spec.loader.exec_module(parsarium)


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


class PilotFormatTest(unittest.TestCase):
    def test_pilot_unresolved_leads_use_status_counts(self):
        self.assertEqual(parsarium.unresolved_count({"leads_by_status": {"unresolved": 7},
                                                     "unresolved_leads": "data/go/mp3/leads.json"}), 7)
        self.assertEqual(parsarium.unresolved_count({"unresolved_documentation_leads": 8}), 8)
        self.assertEqual(parsarium.unresolved_count({"unresolved_leads": 11}), 11)

    def test_registry_keeps_existing_ten_active(self):
        self.assertEqual(len(format_registry.ACTIVE_FORMATS), 10)
        self.assertIn("mp3", format_registry.ACTIVE_FORMATS)
        self.assertNotIn("mp3_id3v2", format_registry.FORMAT_BY_ID)
        self.assertEqual(format_registry.PILOT_FORMATS, ("json", "xml", "yaml"))
        self.assertEqual(format_registry.catalog_format("mp3_id3v2"), "mp3")
        self.assertEqual(len(format_registry.ECOSYSTEMS), 8)

    def test_one_verified_pilot_parser_and_standard_stay_separate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            control = root / "controls/json/tiny.json"
            control.parent.mkdir(parents=True)
            control.write_text('{"ok": true}\n')
            base = root / "data/python/json"
            write(base / "cell.json", {
                "ecosystem": "python", "format": "json",
                "status": "pilot_one_verified_bounded_search_pending",
                "working_target": 10, "ceiling": 10,
                "verified_third_party_count": 1,
                "verified_standard_or_runtime_count": 1,
                "uncertainty": "One valid control; remaining leads unverified.",
            })
            expected = {"ok": True}
            write(base / "parsers.json", [{
                "name": "examplejson", "version": "1.0", "license": "MIT",
                "documentation": "https://example.org/api", "family": "example decoder",
                "input_api": "load(local bytes)", "control": "controls/json/tiny.json",
                "expected_output": expected,
                "metric": {"name": "downloads", "value": 12,
                           "source": "https://example.org/registry"},
            }])
            write(base / "verification.json", {
                "third_party": [{"package": "examplejson", "version": "1.0",
                                 "pass": True, "output": expected}],
                "standard": [{"api": "json.loads(local bytes)", "pass": True,
                              "output": expected}],
            })
            receipt = "projects/json/python/stdlib_json/verification.json"
            write(root / receipt, {"pass": True, "output": expected})
            write(base / "standard.json", {"verified_apis": [{
                "api": "json.loads(local bytes)", "documentation": "https://example.org/stdlib",
                "control": "controls/json/tiny.json", "expected": expected,
                "result": receipt,
            }]})
            with patch.object(build_matrix, "ROOT", root), patch.object(validate_catalog, "ROOT", root):
                build_matrix.main()
                validate_catalog.validate_pilot_cells()
                active = json.loads((root / "data/cells.json").read_text())["cells"]
                pilot = json.loads((root / "data/pilot-cells.json").read_text())["cells"]
                self.assertEqual(len(active), 80)
                self.assertEqual(len(pilot), len(format_registry.ECOSYSTEMS) * len(format_registry.PILOT_FORMATS))
                self.assertEqual(sum(c["verified_third_party_count"] for c in active), 0)
                self.assertEqual(sum(c["verified_third_party_count"] for c in pilot), 1)
                self.assertFalse(next(c for c in pilot if c["ecosystem"] == "python"
                                      and c["format"] == "json")["complete"])
                (root / receipt).unlink()
                with self.assertRaisesRegex(ValueError, "official docs/control"):
                    validate_catalog.validate_pilot_cells()


if __name__ == "__main__":
    unittest.main()
