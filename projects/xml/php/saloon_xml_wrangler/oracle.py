"""Independent expat oracle for the XML Wrangler Element-tree summary.

XML Wrangler keys elements and attributes by raw qualified name and resolves no
namespace URI, so the oracle runs expat without namespace processing: names stay
prefix:local and xmlns/xmlns:* declarations stay ordinary attributes. The
package reports declarations only when their URI is non-empty (veewee/xml's
namespaces() builder skips xmlns=""), so the oracle lists the declarations with
a non-empty value, per element and sorted by attribute name, and keeps the other
attributes in document order. Text is the decoded character data and CDATA of
elements without child elements, untrimmed and including empty strings; text
beside child elements, comments and processing instructions are outside the
package's scope.
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
    state = {"elements": [], "attributes": [], "declarations": [], "text": [],
             "stack": [], "max_depth": 0}

    def start(name, attributes):
        if state["stack"]:
            state["stack"][-1]["children"] = True
        state["elements"].append(name)
        state["stack"].append({"children": False, "text": []})
        state["max_depth"] = max(state["max_depth"], len(state["stack"]))
        declared = []
        for key, value in zip(attributes[::2], attributes[1::2]):
            if key == "xmlns" or key.startswith("xmlns:"):
                if value:
                    declared.append((key, f"{name} {key}={value}"))
            else:
                state["attributes"].append(f"{key}={value}")
        state["declarations"].extend(item for _, item in sorted(declared))

    def end(_name):
        element = state["stack"].pop()
        if not element["children"]:
            state["text"].append("".join(element["text"]))

    def characters(data):
        if state["stack"]:
            state["stack"][-1]["text"].append(data)

    parser.StartElementHandler, parser.EndElementHandler = start, end
    parser.CharacterDataHandler = characters
    parser.Parse(data, True)
    return {"attributes": state["attributes"], "elements": state["elements"],
            "leaf_text": state["text"], "max_depth": state["max_depth"],
            "namespace_declarations": state["declarations"], "root": state["elements"][0]}


def main() -> None:
    for name, digest in CONTROLS.items():
        data = (ROOT / name).read_bytes()
        assert sha256(data).hexdigest() == digest, name
        print(name, json.dumps(summarize(data), ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
