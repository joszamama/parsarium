"""The C JSON star-fallback path (json.h) keeps its tag pin, star record, oracle and parser-scoped feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/c/json"
PROJECT = ROOT / "projects/json/c/json-h"
OVERLAY = ROOT / "fuzzing/afl-native/json/c/json-h"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class CJsonStarFallbackTest(unittest.TestCase):
    def test_tagged_pin_matches_dockerfiles(self) -> None:
        lock = read(PROJECT / "source-lock.json")["json.h"]
        manifest = read(PROJECT / "manifest.json")
        self.assertEqual(lock["release"], manifest["release"])
        self.assertIn("/archive/refs/tags/pre-ai.tar.gz", lock["source"])
        for dockerfile in (PROJECT / "Dockerfile", OVERLAY / "Dockerfile"):
            text = dockerfile.read_text()
            self.assertIn(lock["source"], text)
            self.assertIn(lock["source_sha256"], text)

    def test_star_metric_is_separate_and_recorded(self) -> None:
        row, = [p for p in read(BASE / "parsers.json") if p["name"] == "json.h"]
        popularity = row["popularity"]
        self.assertEqual(row["selection"], "supplemental")
        self.assertEqual(popularity["metric"], "GitHub stars (secondary, repository interest, not downloads)")
        self.assertIsNone(popularity["rank"])
        self.assertGreaterEqual(popularity["value"], 100)
        star_round = read(BASE / "registry-snapshot.json")["round_6_star_fallback"]
        candidate, = [c for c in star_round["candidates"] if c["repository"] == "sheredom/json.h"]
        self.assertEqual(candidate["stargazers_count"], popularity["value"])
        self.assertEqual(candidate["response_sha256"], popularity["response_sha256"])
        self.assertFalse(candidate["fork"])
        self.assertIn("pre-ai", candidate["tags_first5"])
        # Every higher-starred candidate is rejected with a recorded reason.
        higher = [c for c in star_round["candidates"] if c["stargazers_count"] > candidate["stargazers_count"]]
        self.assertTrue(higher)
        self.assertTrue(all(not c["decision"].startswith("selected") for c in higher))
        parson, = [lead for lead in read(BASE / "leads.json") if lead["name"] == "parson"]
        self.assertEqual(parson["status"], "excluded_untagged_release")

    def test_receipts_and_feedback(self) -> None:
        receipt = read(PROJECT / "verification.json")
        overlay = read(OVERLAY / "verification.json")
        diff = read(OVERLAY / "differential.json")
        self.assertTrue(receipt["pass"] and overlay["pass"] and diff["pass"])
        self.assertEqual(overlay["base_project_receipt_sha256"],
                         sha256((PROJECT / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(diff["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(diff["allowlist_entries"], ["src:jsonh-src/json.h"])
        self.assertEqual(diff["no_parse_probe_tuples_per_control"], [0, 0])
        self.assertTrue(diff["repeated_feedback_identical"])
        self.assertGreater(diff["afl_tuple_difference"], 0)
        self.assertGreater(diff["parser_line_difference"], 0)
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(read(BASE / "parsers.json")))


if __name__ == "__main__":
    unittest.main()
