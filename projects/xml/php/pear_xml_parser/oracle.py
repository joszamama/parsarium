"""Independent expat oracle for the pear/xml_parser (XML_Parser) SAX-event summary.

XML_Parser creates its ext/xml parser with xml_parser_create() and no namespace separator, so element and
attribute names are raw qualified names and xmlns/xmlns:* declarations are ordinary attributes. The oracle runs
expat without namespace processing to match that scope: names stay prefix:local and every attribute, declarations
included, is listed as name=value in document order. Character data and CDATA are collected between element
starts, element ends and processing instructions, trimmed of XML whitespace, and empty runs are dropped.
Processing instructions are listed as "target data". Comments and the XML declaration are outside the summary,
because XML_Parser installs no comment handler and the harness defines no default handler.
"""

from hashlib import sha256
import json
from pathlib import Path
from xml.parsers import expat


ROOT = Path(__file__).resolve().parents[4]
CONTROLS = {
    "controls/xml/catalog-ns.xml": "dffe6fcacbea13d5da12b3939756d22cf0a425db8d21c8295ff6a01f8ed22928",
    "controls/xml/order-default-ns.xml": "c0ac18eb0c6e31f6cd920302ac46d9a13959caaa78f2ee7f1f01e0f9a43eccba",
}


def summarize(data: bytes) -> dict:
    parser = expat.ParserCreate("UTF-8")
    parser.ordered_attributes = True
    state = {"elements": [], "attributes": [], "instructions": [], "segments": [], "text": [],
             "depth": 0, "max_depth": 0}

    def flush():
        segment = "".join(state["text"]).strip(" \t\n\r")
        if segment:
            state["segments"].append(segment)
        state["text"] = []

    def start(name, attributes):
        flush()
        state["elements"].append(name)
        state["depth"] += 1
        state["max_depth"] = max(state["max_depth"], state["depth"])
        state["attributes"].extend(f"{key}={value}" for key, value in zip(attributes[::2], attributes[1::2]))

    def end(_name):
        flush()
        state["depth"] -= 1

    def instruction(target, data):
        flush()
        state["instructions"].append(f"{target} {data}")

    parser.StartElementHandler, parser.EndElementHandler = start, end
    parser.CharacterDataHandler = lambda data: state["text"].append(data)
    parser.ProcessingInstructionHandler = instruction
    parser.Parse(data, True)
    return {"attributes": state["attributes"], "elements": state["elements"], "max_depth": state["max_depth"],
            "processing_instructions": state["instructions"], "root": state["elements"][0],
            "text": state["segments"]}


def main() -> None:
    for name, digest in CONTROLS.items():
        data = (ROOT / name).read_bytes()
        assert sha256(data).hexdigest() == digest, name
        print(name, json.dumps(summarize(data), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
