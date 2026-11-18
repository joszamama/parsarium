"""Fuzzing exposure records: one well-formed row per selected third-party path."""

import json
from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import audit_upstream_repositories as upstream_audit  # noqa: E402
import capture_fuzzing_exposure as capture  # noqa: E402

SHA1 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
UTC = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\+00:00$")


class CoverageTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = json.loads(capture.OUT.read_text())
        cls.rows = cls.doc["rows"]
        cls.upstream = json.loads(capture.UPSTREAM.read_text())["rows"]

    def test_exactly_one_row_per_selected_path(self):
        keys = upstream_audit.parser_keys()
        self.assertEqual(set(self.rows), keys)
        counted = []
        for eco in capture.ECOSYSTEMS:
            for path in (ROOT / "data" / eco).glob("*/parsers.json"):
                counted += [f"{eco}/{path.parent.name}/{r['name']}" for r in json.loads(path.read_text())]
        self.assertEqual(len(counted), len(set(counted)), "duplicate parser names in a cell")
        self.assertEqual(len(self.rows), len(counted))
        self.assertEqual(self.doc["summary"]["rows"], len(counted))

    def test_snapshot_metadata(self):
        snap = self.doc["oss_fuzz_snapshot"]
        self.assertRegex(snap["commit"], SHA1)
        self.assertGreater(snap["projects_with_main_repo"], 1000)
        self.assertRegex(self.doc["captured_at_utc"], UTC)
        self.assertIn("heuristic", self.doc["heuristic_label"])

    def test_rows_are_well_formed(self):
        sha = self.doc["oss_fuzz_snapshot"]["commit"]
        for key, row in self.rows.items():
            with self.subTest(key=key):
                eco, fmt, name = key.split("/", 2)
                self.assertEqual((row["ecosystem"], row["format"], row["name"]), (eco, fmt, name))
                self.assertIn(row["collection"], ("active", "pilot"))
                self.assertEqual(row["repository"], self.upstream[key]["repository"])
                rank = row["adoption"]["rank"]
                self.assertTrue(rank is None or rank == "unranked" or rank.rstrip("=").isdigit(), rank)

                oss = row["oss_fuzz"]
                if row["repository"] is None:
                    self.assertEqual((oss["status"], oss["value"], oss["reason"]),
                                     ("not_checked", None, "null_repository"))
                else:
                    self.assertEqual(oss["status"], "checked")
                    self.assertIsInstance(oss["value"], bool)
                    self.assertEqual(oss["value"], bool(oss["projects"]))
                    for p in oss["projects"] + oss.get("name_only_projects", []):
                        self.assertTrue(p["evidence_url"].startswith(
                            f"https://github.com/google/oss-fuzz/blob/{sha}/projects/{p['project']}/"))
                        self.assertRegex(p["project_yaml_sha256"], SHA256)
                    for p in oss["projects"]:
                        self.assertEqual(capture.repo_key(p["main_repo"]), capture.repo_key(row["repository"]))

                harness = row["in_repo_harness"]
                github = bool(row["repository"] and capture.owner_repo(row["repository"]))
                if harness["status"] == "not_checked":
                    self.assertIsNone(harness["value"])
                    self.assertTrue(harness["reason"])
                    if row["repository"] is None:
                        self.assertEqual(harness["reason"], "null_repository")
                    elif not github:
                        self.assertEqual(harness["reason"], "non_github_host")
                    continue
                self.assertTrue(github)
                self.assertIs(harness["heuristic"], True)
                self.assertRegex(harness["repository_commit"], SHA1)
                self.assertRegex(harness["response_sha256"], SHA256)
                self.assertRegex(harness["captured_at_utc"], UTC)
                self.assertIn(harness["repository_commit"], harness["evidence_url"])
                rules = [r["rule"] for r in harness["rules"]]
                self.assertTrue(set(rules) <= set(capture.RULES), rules)
                for r in harness["rules"]:
                    self.assertTrue(1 <= len(r["paths"]) <= capture.MAX_PATHS)
                    self.assertGreaterEqual(r["matches"], len(r["paths"]))
                for probe in harness.get("content_probes", []):
                    self.assertRegex(probe["response_sha256"], SHA256)
                if any(r != "go_fuzz_unknown" for r in rules):
                    self.assertIs(harness["value"], True)
                elif rules or harness["tree_truncated"]:
                    self.assertIsNone(harness["value"])
                else:
                    self.assertIs(harness["value"], False)


class RulesTest(unittest.TestCase):
    def test_tree_rules(self):
        hits = capture.tree_rules([
            "fuzz/Cargo.toml", "fuzz/fuzz_targets/parse.rs", "src/fuzzy_match.py", "tests/test_fuzzy.c",
            "third_party/zlib/contrib/oss-fuzz/inflate_fuzzer.cc", "xml_fuzz_test.go", "tools/xmlfuzz.c",
        ])
        self.assertEqual(hits["fuzz_directory"], ["fuzz"])
        self.assertEqual(hits["cargo_fuzz"], ["fuzz/Cargo.toml"])
        self.assertEqual(hits["fuzz_file"], ["tools/xmlfuzz.c"])

    def test_repo_key_matches_oss_fuzz_forms(self):
        target = capture.repo_key("https://github.com/libexpat/libexpat")
        for raw in ("https://github.com/libexpat/libexpat.git", "git@github.com:libexpat/libexpat.git",
                    "'https://github.com/LibExpat/libexpat'"):
            self.assertEqual(capture.repo_key(raw), target, raw)


if __name__ == "__main__":
    unittest.main()
