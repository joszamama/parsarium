"""Independent expat oracle for the raw-name C XML summaries.

Run without namespace processing, expat reports element and attribute names
as written (prefix:local) and keeps xmlns/xmlns:* declarations as ordinary
attributes in source order. The summary is the root, document-order element
names, maximum depth, attributes as name=decoded value, and trimmed,
non-empty runs of decoded character data and CDATA between markup; comments
and processing instructions end a run. No namespace URI or expanded name is
part of this summary.
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
    state = {"elements": [], "depth": 0, "max_depth": 0, "attributes": [], "text": [], "segments": []}

    def flush(*_) -> None:
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

    parser.StartElementHandler, parser.EndElementHandler = start, end
    parser.CharacterDataHandler = state["text"].append
    parser.CommentHandler = parser.ProcessingInstructionHandler = flush
    parser.Parse(data, True)
    return {"attributes": state["attributes"], "elements": state["elements"],
            "max_depth": state["max_depth"], "root": state["elements"][0],
            "text": state["segments"]}


def main() -> None:
    names = sys.argv[1:] or list(CONTROLS)
    for name in names:
        data = (ROOT / name).read_bytes()
        assert sha256(data).hexdigest() == CONTROLS[name], name
        print(name, json.dumps(summarize(data), ensure_ascii=False, sort_keys=True, separators=(",", ":")))


if __name__ == "__main__":
    main()
