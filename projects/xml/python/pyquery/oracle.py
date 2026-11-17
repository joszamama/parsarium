"""Independent expat oracle for the pyquery summary (copied from projects/xml/python/parsel/oracle.py).

pyquery's contents() walk does not return comments or processing instructions,
so run-control.py compares only the summary keys the harness reports.

The oracle runs CPython's pyexpat (Expat, not libxml2) in namespace mode, so
element and attribute names are {uri}local and xmlns/xmlns:* never appear as
attributes. Each StartNamespaceDecl counts as one declaration (xmlns="" included)
and its non-empty URI joins the namespace set. Character data, CDATA content and
decoded references between two markup events form one text node, matching
libxml2's merged text under lxml's default strip_cdata=True; text is stripped
and kept when non-empty. Comments are stripped, processing instructions are
"target data", and depth counts open elements.

The harness counts in-scope namespace changes, not declarations, so a redundant
redeclaration of an in-scope prefix would count here and not in the harness.
Neither valid control has one.
"""

import json
from pathlib import Path
import sys
from xml.parsers import expat


def expanded(name: str) -> str:
    uri, _, local = name.rpartition(" ")
    return "{" + uri + "}" + local if uri else local


def summarize(data: bytes) -> dict:
    parser = expat.ParserCreate("UTF-8", " ")
    parser.ordered_attributes = True
    state = {"attributes": [], "comments": [], "elements": [], "max_depth": 0,
             "namespace_declarations": 0, "namespaces": set(),
             "processing_instructions": [], "text": []}
    depth = 0
    pending = []

    def flush():
        text = "".join(pending).strip()
        if text:
            state["text"].append(text)
        pending.clear()

    def start(name, attributes):
        nonlocal depth
        flush()
        depth += 1
        state["max_depth"] = max(state["max_depth"], depth)
        state["elements"].append(expanded(name))
        for key, item in zip(attributes[::2], attributes[1::2]):
            state["attributes"].append(expanded(key) + "=" + item)

    def end(_name):
        nonlocal depth
        flush()
        depth -= 1

    def declare(_prefix, uri):
        state["namespace_declarations"] += 1
        if uri:
            state["namespaces"].add(uri)

    def comment(text):
        flush()
        state["comments"].append(text.strip())

    def instruction(target, body):
        flush()
        state["processing_instructions"].append(target + " " + body if body else target)

    parser.StartElementHandler, parser.EndElementHandler = start, end
    parser.StartNamespaceDeclHandler = declare
    parser.CharacterDataHandler = pending.append
    parser.CommentHandler = comment
    parser.ProcessingInstructionHandler = instruction
    parser.Parse(data, True)
    flush()
    state["namespaces"] = sorted(state["namespaces"])
    state["root"] = state["elements"][0]
    return state


if __name__ == "__main__":
    print(json.dumps(summarize(Path(sys.argv[1]).read_bytes()), ensure_ascii=False))
