"""The C plain MP3 libmad path keeps its catalog, lock, receipts, and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/c/mp3"
PROJECT = ROOT / "projects/mp3/c/libmad"
OVERLAY = ROOT / "fuzzing/afl-native/mp3/c/libmad"
sys.path.insert(0, str(ROOT / "controls/mp3"))
from check_controls import walk  # noqa: E402


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class CMp3LibmadPilotTest(unittest.TestCase):
    def test_cell_counts_and_ranked_order(self):
        parsers = read(BASE / "parsers.json")
        leads = {lead["name"]: lead for lead in read(BASE / "leads.json")["leads"]}
        cell = read(BASE / "cell.json")
        self.assertEqual([parser["name"] for parser in parsers], ["mpg123", "libmad"])
        metrics = [parser["metric"]["value"] for parser in parsers]
        self.assertEqual(metrics, sorted(metrics, reverse=True))
        self.assertEqual(len(parsers), cell["verified_third_party_count"])
        self.assertEqual(leads["mad"]["status"], "selected")
        self.assertEqual(leads["mad"]["install_on_request_365d"], parsers[1]["metric"]["value"])
        self.assertEqual(parsers[1]["homebrew_formula"], "mad")
        statuses = {}
        for lead in leads.values():
            statuses[lead["status"]] = statuses.get(lead["status"], 0) + 1
        self.assertEqual(statuses, cell["leads_by_status"])
        self.assertNotEqual(parsers[0]["family"], parsers[1]["family"])

    def test_release_lock_matches_manifest_snapshot_and_dockerfile(self):
        manifest = read(PROJECT / "manifest.json")
        lock = read(PROJECT / "source-lock.json")["libmad"]
        parser = read(BASE / "parsers.json")[1]
        dockerfile = (PROJECT / "Dockerfile").read_text()
        hits = [hit for query in read(BASE / "registry-snapshot.json")["search"]
                for hit in query["hits"] if hit["name"] == "mad"]
        self.assertTrue(hits)
        for hit in hits:
            self.assertEqual(hit["source_url"], lock["source_url"])
            self.assertEqual(hit["source_sha256"], lock["source_sha256"])
            self.assertEqual(hit["license"], lock["license"])
        self.assertEqual(lock["release"], manifest["release"])
        self.assertEqual(lock["release"], parser["version"])
        self.assertEqual(lock["source_sha256"], manifest["source_sha256"])
        self.assertEqual(lock["license"], parser["license"])
        self.assertIn(lock["source_url"], dockerfile)
        self.assertIn(manifest["source_sha256"], dockerfile)
        self.assertIn(manifest["base_image"], dockerfile)

    def test_harness_bounds_guard_padding(self):
        harness = (PROJECT / "harness.c").read_text()
        self.assertIn("calloc(size + MAD_BUFFER_GUARD, 1)", harness)
        self.assertIn("mad_stream_buffer(&stream, buffer, size + MAD_BUFFER_GUARD)", harness)
        self.assertIn("stream.this_frame == buffer + size", harness)
        self.assertIn("result->recoverable_errors++", harness)
        self.assertIn("size > (1u << 20)", harness)

    def test_controls_match_independent_header_walk(self):
        manifest = read(PROJECT / "manifest.json")
        for control, expected in ((manifest["control"], manifest["expected_output"]),
                                  (manifest["differential_control"], manifest["differential_expected_output"])):
            data = (ROOT / control).read_bytes()
            oracle = walk(data)
            self.assertEqual(expected["frames"], oracle["frames"])
            self.assertEqual(expected["sample_rate"], oracle["sample_rate"])
            self.assertEqual(expected["channels"], oracle["channels"])
            self.assertEqual(expected["bit_rate_min"], oracle["bitrate"])
            self.assertEqual(expected["bit_rate_max"], oracle["bitrate"])
            self.assertEqual(expected["decoded_samples"], oracle["frames"] * oracle["samples_per_frame"])
            self.assertEqual(expected["consumed_bytes"], len(data))
            self.assertEqual(expected["input_bytes"], len(data))
            self.assertEqual(expected["recoverable_errors"], 0)

    def test_project_receipt_and_feedback_chain(self):
        manifest = read(PROJECT / "manifest.json")
        receipt = read(PROJECT / "verification.json")
        overlay = read(OVERLAY / "verification.json")
        self.assertTrue(receipt["pass"])
        self.assertEqual(receipt["output"], manifest["expected_output"])
        self.assertEqual(receipt["output"], read(BASE / "parsers.json")[1]["expected_output"])
        self.assertGreater(receipt["format_specific_source_lines_covered"], 0)
        for name, digest in receipt["project_file_sha256"].items():
            self.assertEqual(sha256((PROJECT / name).read_bytes()).hexdigest(), digest, name)
        receipt_digest = sha256((PROJECT / "verification.json").read_bytes()).hexdigest()
        self.assertEqual(overlay["base_project_receipt_sha256"], receipt_digest)
        report = read(BASE / "afl-feedback.json")
        self.assertEqual(report["schema_version"], 2)
        record, = [item for item in report["results"] if item["project"] == "mp3/c/libmad"]
        self.assertTrue(record["pass"] and record["repeated_controls_identical"])
        self.assertEqual(record["base_project_receipt_sha256"], receipt_digest)
        self.assertEqual(record["overlay_receipt_sha256"],
                         sha256((OVERLAY / "verification.json").read_bytes()).hexdigest())
        self.assertEqual(record["first_afl_tuples"], overlay["feedback_edges"])
        self.assertGreater(record["afl_tuple_difference"], 0)
        self.assertEqual(record["second_control_output"], manifest["differential_expected_output"])


if __name__ == "__main__":
    unittest.main()
