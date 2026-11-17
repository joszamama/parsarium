"""The Java XML pilot keeps its selection, leads, runtime path and feedback consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/java/xml"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class JavaXmlPilotTest(unittest.TestCase):
    def test_selected_parsers_are_ranked_and_leads_recorded(self):
        parsers = read(BASE / "parsers.json")
        leads = read(BASE / "leads.json")
        metrics = [parser["popularity"]["value"] for parser in parsers]
        self.assertEqual(metrics, sorted(metrics, reverse=True))
        selected = {f"{parser['group']}:{parser['artifact']}" for parser in parsers}
        self.assertTrue(selected.isdisjoint(
            {lead["coordinate"] for lead in leads if lead["status"] == "unresolved"}))
        self.assertTrue(all(lead["status"] in {"unresolved", "not_a_parser_engine",
                                               "promoted_to_verified"} for lead in leads))
        self.assertEqual({lead["coordinate"] for lead in leads
                          if lead["status"] == "promoted_to_verified"},
                         {"com.fasterxml.woodstox:woodstox-core",
                          "org.dom4j:dom4j",
                          "com.fasterxml:aalto-xml",
                          "com.fasterxml.jackson.dataformat:jackson-dataformat-xml",
                          "org.apache.xmlbeans:xmlbeans",
                          "org.jdom:jdom2", "xom:xom"})
        snapshot = read(BASE / "registry-snapshot.json")
        for parser in parsers:
            coordinate = f"{parser['group']}:{parser['artifact']}"
            recorded = snapshot["popularity_metric"]["packages"][coordinate]
            self.assertEqual(recorded["summed_direct_dependent_count"],
                             parser["popularity"]["value"])
        xerces = next(parser for parser in parsers if parser["artifact"] == "xercesImpl")
        self.assertEqual(snapshot["releases"]["xerces:xercesImpl"]["sources_sha256"],
                         read(ROOT / xerces["project"] / "manifest.json")["source_sha256"])
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], len(parsers))
        self.assertEqual(sum(lead["status"] == "unresolved" for lead in leads),
                         cell["unresolved_documentation_leads"])

    def test_xerces_runtime_family_and_independent_stax_engines(self):
        parsers = read(BASE / "parsers.json")
        xerces = next(parser for parser in parsers if parser["artifact"] == "xercesImpl")
        woodstox = next(parser for parser in parsers if parser["artifact"] == "woodstox-core")
        aalto = next(parser for parser in parsers if parser["artifact"] == "aalto-xml")
        api, = read(BASE / "standard.json")["verified_apis"]
        self.assertIn("Apache Xerces2-J", xerces["shared_families"])
        self.assertNotIn("Apache Xerces2-J", woodstox["shared_families"])
        self.assertIn("Woodstox", woodstox["shared_families"])
        self.assertIn("Aalto XML", aalto["shared_families"])
        self.assertNotIn("Apache Xerces2-J", aalto["shared_families"])
        self.assertIn("Xerces2-J", api["family"])

    def test_dom4j_is_a_wrapper_over_the_jdk_xerces_fork(self):
        parsers = read(BASE / "parsers.json")
        dom4j = next(parser for parser in parsers if parser["group"] == "org.dom4j")
        self.assertEqual(dom4j["shared_families"], ["dom4j", "Apache Xerces2-J"])
        self.assertNotIn("dom4j:dom4j", {f"{p['group']}:{p['artifact']}" for p in parsers})
        legacy = next(lead for lead in read(BASE / "leads.json")
                      if lead["coordinate"] == "dom4j:dom4j")
        self.assertEqual(legacy["status"], "unresolved")
        self.assertEqual(dom4j["popularity"]["value"], 1434)
        project = ROOT / dom4j["project"]
        manifest = read(project / "manifest.json")
        receipt = read(project / "verification.json")
        lock = read(project / "source-lock.json")["dom4j"]
        snapshot = read(BASE / "registry-snapshot.json")["releases"]["org.dom4j:dom4j"]
        self.assertEqual(snapshot["sources_sha256"], manifest["source_sha256"])
        self.assertEqual((snapshot["jar_sha256"], snapshot["pom_sha256"]),
                         (lock["jar_sha256"], lock["pom_sha256"]))
        self.assertEqual(lock["dependencies"], {})
        # dom4j's own package lines are the subject; the JDK fork is reported apart.
        self.assertEqual(manifest["coverage_subject_prefix"], "/work/parser-source/")
        self.assertEqual(manifest["underlying_coverage_subject_prefix"], "/work/underlying-source/")
        self.assertGreater(receipt["parser_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        overlay = (ROOT / "fuzzing/afl-native/xml/java/dom4j/Dockerfile").read_text()
        self.assertIn("ENV PARSARIUM_PARSER_JAR=/work/lib/dom4j-2.2.0.jar", overlay)
        self.assertIn("ENV PARSARIUM_PARSER_SOURCES=/work/parser-source", overlay)

    def test_control_receipts_match_catalog(self):
        parsers = read(BASE / "parsers.json")
        api, = read(BASE / "standard.json")["verified_apis"]
        paths = [(Path(parser["project"]).name, parser["expected_output"])
                 for parser in parsers]
        paths.append(("jdk_documentbuilder", api["expected"]))
        for slug, expected in paths:
            project = ROOT / "projects/xml/java" / slug
            manifest = read(project / "manifest.json")
            receipt = read(project / "verification.json")
            self.assertTrue(receipt["pass"])
            self.assertEqual(receipt["output"], expected)
            self.assertGreater(receipt["parser_source_lines_covered"], 0)
            self.assertEqual(sha256((ROOT / manifest["control"]).read_bytes()).hexdigest(),
                             manifest["control_sha256"])
            for name, digest in receipt["project_file_sha256"].items():
                self.assertEqual(sha256((project / name).read_bytes()).hexdigest(), digest, name)

    def test_xom_source_rebuild_and_underlying_family_are_recorded(self):
        xom = next(parser for parser in read(BASE / "parsers.json")
                   if parser["name"] == "xom")
        self.assertIn("Xerces2-J", xom["family"])
        project = ROOT / xom["project"]
        manifest = read(project / "manifest.json")
        receipt = read(project / "verification.json")
        lock = read(project / "source-lock.json")["xom"]
        self.assertEqual(manifest["source_sha256"], lock["source_sha256"])
        self.assertGreater(receipt["parser_source_lines_covered"], 0)
        self.assertGreater(receipt["underlying_source_lines_covered"], 0)
        self.assertIn("/work/parser-classes", (project / "run-control.sh").read_text())
        self.assertNotIn("/work/build-libs/xerces.jar",
                         manifest["fuzz_smoke_args"][0])

    def test_feedback_is_stable_and_differential(self):
        report = read(BASE / "afl-feedback.json")
        oracle = read(ROOT / "data/go/xml/verification.json")["differential_output"]
        expected_projects = {str(Path(parser["project"]).relative_to("projects"))
                             for parser in read(BASE / "parsers.json") if parser["name"] != "xom"}
        expected_projects.add("xml/java/jdk_documentbuilder")
        aggregated = {item["project"] for item in report["results"]}
        self.assertIn(aggregated, (expected_projects,
                                   expected_projects | {"xml/java/xom"}))
        self.assertEqual(report["projects_passed"], len(aggregated))
        for result in report["results"]:
            overlay = ROOT / "fuzzing/afl-native" / result["project"] / "verification.json"
            self.assertEqual(sha256(overlay.read_bytes()).hexdigest(), result["overlay_receipt_sha256"])
            self.assertTrue(result["pass"] and result["repeated_control_identical"])
            self.assertGreater(result["parser_feature_difference"], 0)
            self.assertGreater(result["afl_tuple_difference"], 0)
            if result["project"].endswith("/jackson_xml"):
                self.assertEqual(result["differential_output"]["token_count"], 25)
                self.assertEqual(len(result["differential_output"]["events"]), 25)
            else:
                self.assertEqual(result["differential_output"], oracle)
        xom = read(ROOT / "fuzzing/afl-native/xml/java/xom/differential.json")
        self.assertEqual(xom["differential_output"], oracle)
        self.assertTrue(xom["pass"] and xom["repeated_control_identical"]
                        and xom["repeated_differential_identical"])
        self.assertGreater(xom["parser_feature_difference"], 0)
        self.assertGreater(xom["afl_tuple_difference"], 0)
        overlay = ROOT / "fuzzing/afl-native/xml/java/xom/verification.json"
        self.assertEqual(sha256(overlay.read_bytes()).hexdigest(),
                         xom["overlay_receipt_sha256"])


if __name__ == "__main__":
    unittest.main()
