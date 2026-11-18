"""The engine map covers every parser path once and follows the relation rule."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from audit_engines import load, problems  # noqa: E402
from audit_upstream_repositories import parser_keys  # noqa: E402


class EngineMapTests(unittest.TestCase):
    def test_committed_maps_are_clean(self) -> None:
        self.assertEqual(problems(load(), parser_keys()), [])

    def test_rules_catch_mistakes(self) -> None:
        bad = [{"format": "png", "engines": {"libpng": {"language": "c", "repository": "http://x"},
                                             "unused": {"language": "go", "repository": None}},
                "paths": [{"path": "php/png/a", "engine": "libpng", "relation": "wrapper",
                           "confidence": "high", "evidence": "e"},
                          {"path": "php/png/a", "engine": "missing", "relation": "own",
                           "confidence": "high", "evidence": "e"}]}]
        found = "\n".join(problems(bad, {"php/png/a", "php/png/b"}))
        for expected in ("not https", "use binding", "not defined", "defined but not used",
                         "php/png/b: no engine row", "2 engine rows"):
            self.assertIn(expected, found)


if __name__ == "__main__":
    unittest.main()
