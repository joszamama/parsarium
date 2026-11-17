"""Independent expat oracle for the htmlparser2 raw-name summary.

htmlparser2 does not resolve namespaces, so the oracle runs expat without
namespace processing: element and attribute names stay qualified names
(prefix:local), and xmlns/xmlns:* declarations stay ordinary attributes in
source order. Text is trimmed, non-empty runs of decoded character data and
CDATA between markup. htmlparser2 reports the XML declaration through its
processing-instruction callback, so the oracle takes expat's raw declaration
text from the default handler and reports it in the same list.
"""

from hashlib import sha256
import json
from pathlib import Path
import sys
from xml.parsers import expat


ROOT = Path(__file__).resolve().parents[4]
CONTROLS = {
    "controls/xml/catalog-ns.xml": "dffe6fcacbea13d5da12b3939756d22cf0a425db8d21c8295ff6a01f8ed22928",
    "controls/xml/order-default-ns.xml": "c0ac18eb0c6e31f6cd920302ac46d9a13959caaa78f2ee7f1f01e0f9a43eccba",
}


def summarize(data: bytes) -> dict:
    parser = expat.ParserCreate("UTF-8")
    parser.ordered_attributes = True
    state = {"elements": [], "depth": 0, "max_depth": 0, "attributes": [], "text": [],
             "segments": [], "comments": [], "instructions": [], "cdata": 0}

    def flush() -> None:
        segment = "".join(state["text"]).strip()
        if segment:
            state["segments"].append(segment)
        state["text"].clear()

    def start(name, attributes):
        flush()
        state["elements"].append(name)
        state["depth"] += 1
        state["max_depth"] = max(state["max_depth"], state["depth"])
        for key, value in zip(attributes[::2], attributes[1::2]):
            state["attributes"].append(f"{key}={value}")

    def end(_name):
        flush()
        state["depth"] -= 1

    def comment(text):
        flush()
        state["comments"].append(text)

    def instruction(target, text):
        flush()
        state["instructions"].append(f"{target} {text}" if text else target)

    def default(raw):
        # Without an XmlDeclHandler, expat passes the declaration here verbatim.
        if raw.startswith("<?xml") and raw.endswith("?>"):
            state["instructions"].append(raw[2:-2])

    def cdata():
        state["cdata"] += 1

    parser.StartElementHandler, parser.EndElementHandler = start, end
    parser.CharacterDataHandler = state["text"].append
    parser.CommentHandler = comment
    parser.ProcessingInstructionHandler = instruction
    parser.StartCdataSectionHandler = cdata
    parser.DefaultHandlerExpand = default
    parser.Parse(data, True)
    return {"attributes": state["attributes"], "cdata_sections": state["cdata"],
            "comments": state["comments"], "elements": state["elements"],
            "max_depth": state["max_depth"],
            "processing_instructions": state["instructions"],
            "root": state["elements"][0], "text": state["segments"]}


def main() -> None:
    outputs = {}
    for name, digest in CONTROLS.items():
        data = (ROOT / name).read_bytes()
        if sha256(data).hexdigest() != digest:
            raise SystemExit(f"control hash mismatch: {name}")
        outputs[name] = summarize(data)
    json.dump(outputs, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
