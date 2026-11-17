"""Go XML lead exclusions keep their overlap, valid-control and own-feedback evidence consistent."""

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "data/go/xml"
GH = "github.com/"


def read(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


class GoXmlLeadDecisionTest(unittest.TestCase):
    def setUp(self):
        self.leads = {lead["name"]: lead for lead in read(BASE / "leads.json")}
        self.overlap = read(BASE / "lead-overlap-check.json")
        self.gates = read(BASE / "wrapper-gates-check.json")

    def overlap_of(self, lead: str, reference_prefix: str) -> float:
        result, = [item for item in self.overlap["results"]
                   if item["lead"] == lead and item["reference"].startswith(reference_prefix)]
        return result["overlap"]

    def test_overlap_receipt_matches_script(self):
        script = ROOT / "scripts/check_go_xml_lead_overlap.py"
        self.assertEqual(self.overlap["script_sha256"], sha256(script.read_bytes()).hexdigest())
        for lead, reference in ((GH + "clbanning/mxj/v2", GH + "clbanning/mxj (selected)"),
                                (GH + "jbowtie/gokogiri/xml", GH + "moovweb/gokogiri/xml"),
                                (GH + "clbanning/x2j", GH + "beego/x2j"),
                                (GH + "nbio/xml", GH + "vmware/govmomi"),
                                (GH + "samuel-jimenez/xml", GH + "vmware/govmomi"),
                                (GH + "minio/xxml", GH + "vmware/govmomi"),
                                (GH + "printesoi/xml-go", GH + "vmware/govmomi"),
                                (GH + "mattn/go-pkg-xmlx", GH + "go-forks/go-pkg-xmlx"),
                                (GH + "zhuxiujia/GoMybatis/lib/github.com/beevik/etree", GH + "beevik/etree v1.0.1")):
            self.assertGreaterEqual(self.overlap_of(lead, reference), 0.7, lead)
        mattn, = [item for item in self.overlap["results"] if item["lead"] == GH + "mattn/go-pkg-xmlx"]
        self.assertEqual(mattn["byte_identical_files"], mattn["candidate_files"])

    def test_wrapper_gates(self):
        results = self.gates["results"]
        for name in ("goxml2json-decode", "simplexml-dom", "go-xmldom"):
            self.assertEqual(results[name]["own_block_difference"], 0, name)
        self.assertTrue(all(block.startswith(GH + "basgys/goxml2json/encoder.go:")
                            for block in results["goxml2json-convert"]["changed_blocks"]))
        catalog = "controls/xml/catalog-ns.xml"
        self.assertNotIn("x < y", json.dumps(results["quickxml"]["observed"][catalog], ensure_ascii=False))
        self.assertIn("&amp;", json.dumps(results["quickxml"]["observed"][catalog], ensure_ascii=False))
        self.assertNotIn("a1", json.dumps(results["xml2map"]["observed"][catalog]))
        probe = ROOT / "lead-probes/go/xml/wrapper-gates"
        for name, digest in self.gates["probe_file_sha256"].items():
            self.assertEqual(sha256((probe / name).read_bytes()).hexdigest(), digest, name)
        for control, digest in self.gates["control_sha256"].items():
            self.assertEqual(sha256((ROOT / control).read_bytes()).hexdigest(), digest)

    def test_lead_statuses(self):
        excluded = (GH + "basgys/goxml2json", GH + "clbanning/mxj/v2", GH + "jbowtie/gokogiri/xml",
                    GH + "clbanning/x2j", GH + "nbio/xml", GH + "tdewolff/parse/v2/xml",
                    GH + "VictorLowther/simplexml/dom", GH + "subchen/go-xmldom", GH + "sbabiv/xml2map",
                    GH + "dgrr/quickxml", GH + "mattn/go-pkg-xmlx", GH + "lestrrat/go-libxml2")
        for name in excluded:
            self.assertEqual(self.leads[name]["status"], "excluded", name)
        selected = {parser["name"] for parser in read(BASE / "parsers.json")}
        self.assertEqual(len(selected), 10)
        cut = min(parser["popularity"]["value"] for parser in read(BASE / "parsers.json"))
        # Every lead above the tenth path's metric is decided, not left open.
        for lead in self.leads.values():
            if (lead.get("imported_by") or 0) > cut:
                self.assertIn(lead["status"], {"excluded", "promoted_to_verified"}, lead["name"])
        cell = read(BASE / "cell.json")
        self.assertEqual(cell["verified_third_party_count"], 10)
        self.assertEqual(cell["unresolved_documentation_leads"],
                         sum(lead["status"] == "unresolved" for lead in self.leads.values()))


if __name__ == "__main__":
    unittest.main()
