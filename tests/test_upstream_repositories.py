"""Upstream repository links: URL normalization and catalog coverage."""

import copy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_upstream_repositories as audit  # noqa: E402
from capture_upstream_repositories import normalize_repo  # noqa: E402


class NormalizeRepoTest(unittest.TestCase):
    def test_registry_forms(self):
        cases = {
            "git+https://github.com/visgl/loaders.gl.git": "https://github.com/visgl/loaders.gl",
            "git://github.com/a/b.git": "https://github.com/a/b",
            "git@github.com:a/b.git": "https://github.com/a/b",
            "github:a/b": "https://github.com/a/b",
            "https://github.com/serde-rs/json/tree/v1.0.154": "https://github.com/serde-rs/json",
            "https://codeload.github.com/flow-php/postgresql/legacy.zip/f28a": "https://github.com/flow-php/postgresql",
            "https://api.github.com/repos/sheredom/json.h": "https://github.com/sheredom/json.h",
            "https://gitlab.gnome.org/GNOME/libxml2/-/tags/v2.15.4": "https://gitlab.gnome.org/GNOME/libxml2",
            "https://gitbox.apache.org/repos/asf/commons-compress.git":
                "https://gitbox.apache.org/repos/asf?p=commons-compress.git",
            "https://sourceforge.net/projects/rapidxml/files/": "https://sourceforge.net/projects/rapidxml/",
        }
        for raw, expected in cases.items():
            self.assertEqual(normalize_repo(raw), expected, raw)

    def test_rejects_non_repositories(self):
        for raw in ("https://github.com/conan-io/conan-center-index/blob/master/recipes/x/conanfile.py",
                    "https://salsa.debian.org/debian/jansson", "https://pypi.org/project/x/",
                    "https://github.com/orgs/x", "http://example.org/x", None):
            self.assertIsNone(normalize_repo(raw), raw)


class CoverageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(audit.DATA.read_text())
        cls.keys = audit.parser_keys()

    def test_catalog_is_covered(self):
        self.assertEqual(audit.problems(self.doc, self.keys), [])

    def test_missing_row_http_url_and_bare_null_are_reported(self):
        doc = copy.deepcopy(self.doc)
        rows = doc["rows"]
        first, second, third = sorted(rows)[:3]
        del rows[first]
        rows[second]["repository"] = rows[second]["repository"] and rows[second]["repository"].replace(
            "https://", "http://") or "http://example.org/x"
        rows[third].update(repository=None, repository_note=None, source=None)
        found = audit.problems(doc, self.keys)
        self.assertIn(f"missing upstream row: {first}", found)
        self.assertIn(f"repository is not https: {second}", found)
        self.assertIn(f"no repository and no repository_note: {third}", found)


if __name__ == "__main__":
    unittest.main()
