"""The Java TOML pilot keeps its selection, leads, receipts and AFL++ feedback consistent."""

from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/java/toml"
CONTROL = "controls/toml/service-config.toml"
DIFFERENTIAL = "controls/toml/typed-scalars.toml"
SELECTED = ["jackson-dataformat-toml", "tomlj", "night-config-toml", "jtoml", "ktoml-core"]


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def check_project(test: unittest.TestCase, slug: str) -> None:
    """Static receipt, manifest, lock, overlay and feedback consistency for one selected path."""
    project = ROOT / "projects/toml/java" / slug
    manifest = read(project / "manifest.json")
    receipt = read(project / "verification.json")
    parser, = [item for item in read(BASE / "parsers.json") if item["project"] == f"projects/toml/java/{slug}"]
    lock = read(project / "source-lock.json")[manifest["package"]]
    test.assertEqual((manifest["format"], manifest["ecosystem"]), ("toml", "java"))
    test.assertEqual(parser["name"], manifest["package"])
    test.assertEqual(parser["version"], manifest["release"])
    test.assertEqual(lock["release"], manifest["release"])
    test.assertEqual(lock["source_sha256"], manifest["source_sha256"])
    test.assertEqual(parser["license"], lock["license"])
    # Both controls are pinned and their expected trees are the committed hand-written trees.
    test.assertEqual(manifest["control"], CONTROL)
    test.assertEqual(manifest["differential_control"], DIFFERENTIAL)
    for key in ("control", "differential_control"):
        test.assertEqual(sha256((ROOT / manifest[key]).read_bytes()).hexdigest(), manifest[f"{key}_sha256"])
    test.assertEqual(manifest["expected_output"], read(ROOT / "controls/toml/service-config.expected.json"))
    test.assertEqual(manifest["differential_expected_output"],
                     read(ROOT / "controls/toml/typed-scalars.expected.json"))
    test.assertEqual(parser["expected_output"], manifest["expected_output"])
    test.assertEqual(parser["differential_expected_output"], manifest["differential_expected_output"])
    # The Dockerfile verifies every downloaded jar against the lock and manifest digests.
    dockerfile = (project / "Dockerfile").read_text()
    for digest in (manifest["base_image"], manifest["source_sha256"], lock["jar_sha256"],
                   manifest["fuzz_engine_sha256"], *(dep["jar_sha256"] for dep in lock["runtime_dependencies"])):
        test.assertIn(digest, dockerfile)
    # Project receipt: current files, both outputs, own parser source lines only.
    test.assertTrue(receipt["pass"] and receipt["fuzz_engine_smoke_pass"])
    test.assertEqual(receipt["output"], manifest["expected_output"])
    test.assertEqual(receipt["control_sha256"], manifest["control_sha256"])
    test.assertEqual(receipt["source_sha256"], manifest["source_sha256"])
    test.assertGreater(receipt["parser_source_files"], 0)
    test.assertGreater(receipt["parser_source_lines_covered"], 0)
    for name, digest in receipt["project_file_sha256"].items():
        test.assertEqual(sha256((project / name).read_bytes()).hexdigest(), digest, name)
    includes = re.search(r"includes=(\S+?) ", (project / "run-control.sh").read_text()).group(1)
    package_prefix = includes.removesuffix(".*").replace(".", "/") + "/"
    # AFL++ overlay is bound to the current project receipt and scoped to the same package.
    overlay = ROOT / "fuzzing/afl-native/toml/java" / slug
    overlay_receipt = read(overlay / "verification.json")
    test.assertTrue(overlay_receipt["pass"])
    test.assertEqual(overlay_receipt["base_project_receipt_sha256"],
                     sha256((project / "verification.json").read_bytes()).hexdigest())
    test.assertEqual(overlay_receipt["base_image_id"], receipt["image_id"])
    test.assertEqual(overlay_receipt["control_sha256"], manifest["control_sha256"])
    test.assertEqual(overlay_receipt["parser_source_features"], receipt["parser_source_lines_covered"])
    test.assertIn(f"ENV PARSARIUM_JACOCO_INCLUDES={includes}\n", (overlay / "Dockerfile").read_text())
    for name, digest in overlay_receipt["overlay_file_sha256"].items():
        test.assertEqual(sha256((overlay / name).read_bytes()).hexdigest(), digest, name)
    for name, digest in overlay_receipt["bridge_file_sha256"].items():
        test.assertEqual(sha256((ROOT / "fuzzing/afl-bridge" / name).read_bytes()).hexdigest(), digest, name)
    # Feedback: stable repeats, the two controls differ, lines are per parser file.
    feedback, = [row for row in read(BASE / "afl-feedback.json")["results"]
                 if row["project"] == f"toml/java/{slug}"]
    test.assertTrue(feedback["pass"])
    test.assertEqual(feedback["overlay_receipt_sha256"],
                     sha256((overlay / "verification.json").read_bytes()).hexdigest())
    test.assertEqual(feedback["base_project_receipt_sha256"], overlay_receipt["base_project_receipt_sha256"])
    test.assertGreaterEqual(feedback["repeats_per_control"], 3)
    test.assertTrue(feedback["repeated_control_identical"] and feedback["repeated_differential_identical"])
    test.assertEqual(feedback["control_afl_tuples"], overlay_receipt["feedback_edges"])
    test.assertEqual(feedback["control_parser_lines"], receipt["parser_source_lines_covered"])
    test.assertGreaterEqual(feedback["afl_tuple_difference"], 2)
    test.assertGreaterEqual(feedback["parser_line_difference"], 2)
    test.assertEqual(feedback["afl_tuple_difference"],
                     feedback["afl_tuples_only_in_control"] + feedback["afl_tuples_only_in_differential"])
    test.assertEqual(feedback["differential_output"], manifest["differential_expected_output"])
    for key, total in (("control_parser_lines_per_file", "control_parser_lines"),
                       ("differential_parser_lines_per_file", "differential_parser_lines")):
        test.assertEqual(sum(feedback[key].values()), feedback[total])
        test.assertTrue(all(name.startswith(package_prefix) for name in feedback[key]), key)


class JavaTomlPilotTest(unittest.TestCase):
    def test_selection_is_ranked_by_recorded_metric(self):
        parsers = read(BASE / "parsers.json")
        self.assertEqual([parser["name"] for parser in parsers], SELECTED)
        snapshot = read(BASE / "registry-snapshot.json")["popularity_metric"]
        values = []
        for parser in parsers:
            recorded = snapshot["packages"][parser["coordinate"]]
            self.assertEqual(parser["metric"]["value"], recorded["summed_direct_dependent_count"])
            self.assertEqual(parser["metric"]["name"], snapshot["name"])
            self.assertTrue(parser["family"] and parser["family_note"] and parser["input_api"])
            values.append(parser["metric"]["value"])
        self.assertEqual(values, sorted(values, reverse=True))
        self.assertEqual(len({parser["family"] for parser in parsers}), len(parsers))
        jackson = parsers[0]
        self.assertIn("PARSE_JAVA_TIME", jackson["input_api"])
        self.assertIn("Java JSON cell", jackson["family_note"])

    def test_leads_keep_failure_evidence_and_exclude_selected(self):
        parsers = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")["leads"]
        self.assertFalse({parser["coordinate"] for parser in parsers} & {lead["name"] for lead in leads})
        self.assertTrue(all(lead["status"].startswith("unresolved") for lead in leads))
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["unresolved_documentation_leads"], len(leads))
        self.assertEqual(cell["leads_by_status"], dict(Counter(lead["status"] for lead in leads)))
        toml4j, = [lead for lead in leads if lead["name"] == "com.moandjiezana.toml:toml4j"]
        self.assertEqual(toml4j["status"], "unresolved_control_failed")
        probe = read(ROOT / toml4j["probe"])
        self.assertEqual(probe["release"], toml4j["version_seen"])
        self.assertEqual(sha256((ROOT / probe["probe_source"]).read_bytes()).hexdigest(),
                         probe["probe_source_sha256"])
        primary, second = probe["cases"]
        for case in probe["cases"]:
            self.assertEqual(sha256((ROOT / case["control"]).read_bytes()).hexdigest(), case["control_sha256"])
        self.assertTrue(primary["matches_expected_tree"])
        self.assertFalse(second["matches_expected_tree"])
        self.assertIn("key hex on line 6", second["error"])
        # Every remaining lead is below the lowest selected metric or has none.
        lowest = min(parser["metric"]["value"] for parser in parsers)
        self.assertTrue(all(lead["metric_value"] is None or lead["metric_value"] < lowest
                            for lead in leads if lead["status"] == "unresolved_not_run"))

    def test_cell_counts_and_control_results_match(self):
        parsers = read(BASE / "parsers.json")
        cell = read(BASE / "cell.json")
        verification = read(BASE / "verification.json")
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(cell["verified_standard_or_runtime_count"], 0)
        self.assertEqual(read(BASE / "standard.json")["verified_apis"], [])
        records = {item["package"]: item for item in verification["third_party"]}
        self.assertEqual(set(records), {parser["name"] for parser in parsers})
        for parser in parsers:
            record = records[parser["name"]]
            self.assertTrue(record["pass"])
            self.assertEqual(record["version"], parser["version"])
            self.assertEqual(record["output"], parser["expected_output"])
            self.assertEqual(record["differential_output"], parser["differential_expected_output"])
            self.assertEqual(read(ROOT / record["project_receipt"])["output"], parser["expected_output"])

    def test_ranking_table_header_and_rows(self):
        text = (BASE / "ranking.md").read_text(encoding="utf-8")
        self.assertIn("| Rank | Package | Release | Metric | Parsed scope | Parser family |", text)
        for rank, parser in enumerate(read(BASE / "parsers.json"), 1):
            self.assertIn(f"| {rank} | [{parser['name']}]({parser['documentation']}) | {parser['version']} | "
                          f"{parser['metric']['value']:,} |", text)
        self.assertIn("toml4j", text.split("## Unverified leads", 1)[1])


if __name__ == "__main__":
    unittest.main()
