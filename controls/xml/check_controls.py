"""Check XML controls with expat, independently of the parser harnesses.

The files are hand-written XML 1.0 in UTF-8, without a DOCTYPE. This script
parses them with the Python standard library's expat binding in namespace mode
and builds the same summary the quick-xml harness reports: the root and
document-order element expanded names, the maximum depth, namespace
declarations, non-declaration attributes, and trimmed, non-empty runs of decoded
character data between markup. It is the oracle for the expected outputs.
"""

from hashlib import sha256
import json
from pathlib import Path
from xml.parsers import expat

ROOT = Path(__file__).resolve().parent
CONTROLS = {
    "catalog-ns.xml": "dffe6fcacbea13d5da12b3939756d22cf0a425db8d21c8295ff6a01f8ed22928",
    "order-default-ns.xml": "c0ac18eb0c6e31f6cd920302ac46d9a13959caaa78f2ee7f1f01e0f9a43eccba",
    "order-default-ns-no-pi.xml": "b8b364b48cb3b03a82611917fd6344edfbd80789eb29203cdf6814d96f354d9b",
    "order-default-ns-restricted.xml": "00a42bfc046d919d0262460ac00b8e8a4ce5d553f4581b58006ef619ebf93f53",
}


def clark(name: str) -> str:
    uri, _, local = name.rpartition(" ")
    return f"{{{uri}}}{local}" if uri else local


def summarize(data: bytes) -> dict:
    parser = expat.ParserCreate("UTF-8", " ")
    parser.ordered_attributes = True
    state = {"elements": [], "depth": 0, "max_depth": 0, "declarations": 0,
             "namespaces": set(), "attributes": [], "text": [], "segments": []}

    def flush(*_):
        segment = "".join(state["text"]).strip()
        if segment:
            state["segments"].append(segment)
        state["text"].clear()

    def start(name, attributes):
        flush()
        state["elements"].append(clark(name))
        state["depth"] += 1
        state["max_depth"] = max(state["max_depth"], state["depth"])
        for key, value in zip(attributes[::2], attributes[1::2]):
            state["attributes"].append(f"{clark(key)}={value}")

    def end(_name):
        flush()
        state["depth"] -= 1

    def declare(_prefix, uri):
        state["declarations"] += 1
        if uri:
            state["namespaces"].add(uri)

    parser.StartElementHandler, parser.EndElementHandler = start, end
    parser.StartNamespaceDeclHandler = declare
    parser.CharacterDataHandler = state["text"].append
    parser.CommentHandler = parser.ProcessingInstructionHandler = flush
    parser.Parse(data, True)
    return {"attributes": state["attributes"], "elements": state["elements"],
            "max_depth": state["max_depth"], "namespace_declarations": state["declarations"],
            "namespaces": sorted(state["namespaces"]), "root": state["elements"][0],
            "text": state["segments"]}


if __name__ == "__main__":
    for name, digest in CONTROLS.items():
        data = (ROOT / name).read_bytes()
        assert sha256(data).hexdigest() == digest, name
        data.decode("utf-8")
        print(name, json.dumps(summarize(data), ensure_ascii=False, sort_keys=True, separators=(",", ":")))
