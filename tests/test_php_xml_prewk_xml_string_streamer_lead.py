"""prewk/xml-string-streamer is a negative lead: getNode() returns raw byte slices, not parsed XML."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/php/xml"
PROBE = ROOT / "lead-probes/php/xml/prewk_xml_string_streamer"
CHECK = BASE / "prewk-xml-string-streamer-lead-check.json"
APIS = ("createStringWalkerParser(path)", "StringWalker+Stream\\File(handle)", "createUniqueNodeParser(path)")


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


class PhpXmlPrewkXmlStringStreamerLeadTest(unittest.TestCase):
    def test_lead_is_pinned_and_not_counted_as_a_parser(self):
        check = read(CHECK)
        self.assertEqual(check["status"], "negative_lead_raw_node_string_splitter")
        lead, = [item for item in read(BASE / "leads.json") if item["name"] == check["package"]]
        self.assertEqual((lead["version_seen"], lead["packagist_downloads"], lead["license"]),
                         (check["release"], check["popularity"]["value"], check["license"]))
        self.assertNotIn(check["package"], {item["name"] for item in read(BASE / "parsers.json")})
        self.assertFalse((ROOT / "projects/xml/php/prewk_xml_string_streamer").exists())
        locked, = read(PROBE / "composer.lock")["packages"]
        self.assertEqual((locked["version"], locked["source"]["reference"]),
                         (check["release"], check["composer_reference"]))
        dockerfile = (PROBE / "Dockerfile").read_text()
        self.assertIn(check["archive_sha256"], dockerfile)
        self.assertIn(check["composer_reference"], dockerfile)
        for name, digest in check["probe_file_sha256"].items():
            self.assertEqual(sha256((PROBE / name).read_bytes()).hexdigest(), digest, name)
        self.assertEqual(check["source_api_mentions"], {"preg_match": [
            "src/XmlStringStreamer/Stream/File.php", "src/XmlStringStreamer/Parser/StringWalker.php",
            "src/XmlStringStreamer/Parser/UniqueNode.php"]})
        self.assertTrue(check["afl_feedback"].startswith("not_run"))

    def test_every_node_is_a_verbatim_slice_of_the_control(self):
        check = read(CHECK)
        controls = {}
        for name, digest in check["control_sha256"].items():
            controls[name] = (ROOT / "controls/xml" / name).read_bytes()
            self.assertEqual(sha256(controls[name]).hexdigest(), digest)
        runs = {(run["control"], run["api"]): run for run in check["observed"]}
        self.assertEqual(set(runs), {(control, api) for control in controls for api in APIS})
        self.assertTrue(check["nodes_match_byte_span_oracle"])
        for (control, _), run in runs.items():
            for node in run["nodes"]:
                start, end = node["byte_span"]
                self.assertEqual(controls[control][start:end].decode("utf-8"), node["text"])
        walker = [node["text"] for node in runs["order-default-ns.xml", APIS[0]]["nodes"]]
        self.assertEqual(walker[0], '\n  <?audit step="1"?>')
        self.assertIn("&#x2D;", walker[1])
        item = runs["catalog-ns.xml", APIS[2]]["nodes"][0]
        self.assertEqual(item["text"], '<item id="a1" c:lang="es">Café &amp; té</item>')
        self.assertEqual(item["outside_namespace_bindings_used"],
                         [["", "urn:parsarium:item"], ["c", "urn:parsarium:catalog"]])
        self.assertEqual(runs["catalog-ns.xml", APIS[0]]["nodes"][0]["text"],
                         "\n  " + item["text"])

    def test_only_the_root_pi_branch_differs_between_controls(self):
        differential = read(CHECK)["splitter_line_differential"]
        self.assertEqual(differential[APIS[1]]["only_order-default-ns.xml"], [250, 251])
        self.assertEqual(differential[APIS[1]]["only_catalog-ns.xml"], [])


if __name__ == "__main__":
    unittest.main()
