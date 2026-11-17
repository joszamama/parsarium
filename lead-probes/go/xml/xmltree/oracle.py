"""Project the two valid XML controls onto the fields aqwari.net/xml/xmltree exposes.

The oracle uses the Python standard library's expat binding in namespace mode
with prefixes reported, not Go encoding/xml. It records expanded and qualified
element and attribute names in document order (namespace declarations are not
attributes, as in xmltree), maximum depth, URIs used by element and attribute
names, and the raw source bytes between the start and end tag of every leaf
element. Raw bytes are sliced from expat's byte offsets; character and entity
references and CDATA markup stay undecoded, as in xmltree's Element.Content.

Run with: python3 -I lead-probes/go/xml/xmltree/oracle.py [CONTROL ...]
"""

import json
from pathlib import Path
import sys
from xml.parsers import expat

ROOT = Path(__file__).resolve().parents[4]
CONTROLS = ("controls/xml/catalog-ns.xml", "controls/xml/order-default-ns.xml")


def start_tag_end(data: bytes, start: int) -> int:
    """Return the offset just past the '>' that closes the start tag at start."""
    quote = None
    for index in range(start + 1, len(data)):
        byte = data[index:index + 1]
        if quote:
            if byte == quote:
                quote = None
        elif byte in (b'"', b"'"):
            quote = byte
        elif byte == b">":
            return index + 1
    raise ValueError("unterminated start tag")


def summarize(data: bytes) -> dict:
    parser = expat.ParserCreate("UTF-8", " ")
    parser.namespace_prefixes = True
    parser.ordered_attributes = True
    names = set()
    out = {"elements": [], "element_qnames": [], "attributes": [], "attribute_qnames": [],
           "leaf_content": [], "max_depth": 0}
    stack = []

    def split(name: str) -> tuple[str, str]:
        parts = name.split(" ")
        if len(parts) == 1:
            return parts[0], parts[0]
        names.add(parts[0])
        clark = "{" + parts[0] + "}" + parts[1]
        return clark, (parts[2] + ":" + parts[1]) if len(parts) == 3 else parts[1]

    def start(name, attributes):
        if stack:
            stack[-1]["leaf"] = False
        clark, qname = split(name)
        out["elements"].append(clark)
        out["element_qnames"].append(qname)
        for key, value in zip(attributes[::2], attributes[1::2]):
            attribute_clark, attribute_qname = split(key)
            out["attributes"].append(f"{attribute_clark}={value}")
            out["attribute_qnames"].append(f"{attribute_qname}={value}")
        begin = start_tag_end(data, parser.CurrentByteIndex)
        stack.append({"name": clark, "begin": begin, "leaf": True,
                      "empty": data[begin - 2:begin] == b"/>"})
        out["max_depth"] = max(out["max_depth"], len(stack))

    def end(_name):
        element = stack.pop()
        if element["leaf"]:
            raw = b"" if element["empty"] else data[element["begin"]:parser.CurrentByteIndex]
            out["leaf_content"].append(f"{element['name']}={raw.decode('utf-8')}")

    parser.StartElementHandler = start
    parser.EndElementHandler = end
    parser.Parse(data, True)
    out["name_namespaces"] = sorted(names)
    out["root"] = out["elements"][0]
    return out


def main() -> None:
    controls = sys.argv[1:] or CONTROLS
    print(json.dumps({control: summarize((ROOT / control).read_bytes()) for control in controls},
                     indent=2, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
