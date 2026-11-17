"""Parse one local XML file through the documented jxmlease.parse(xml_input) API.

jxmlease 1.0.3's Parser creates a CPython pyexpat parser itself
(xml.parsers.expat.ParserCreate) and builds XMLDictNode / XMLListNode /
XMLCDATANode objects in its own _DictSAXHandler. With the default
process_namespaces=False, Expat reports names as written, so element and
attribute names are raw qualified names (prefix:local) and xmlns/xmlns:*
declarations stay ordinary attributes. This is a raw-name view: no namespace
URI is resolved. The summary walks the returned node tree only through the
documented node API (dict/list traversal, tag, get_xml_attrs, get_cdata).
"""

import os
from pathlib import Path
import tempfile
from xml.parsers import expat

import jxmlease

PARSE_ERRORS = (expat.ExpatError, ValueError, UnicodeError)


def parse_tree(path):
    return jxmlease.parse(Path(path).read_bytes())


def summarize(document):
    roots = list(document.values())
    if len(roots) != 1:
        return None
    state = {"attributes": [], "elements": [], "max_depth": 0, "text": []}

    def visit(node, depth):
        if isinstance(node, jxmlease.XMLListNode):
            for item in node:
                visit(item, depth)
            return
        state["elements"].append(node.tag)
        state["max_depth"] = max(state["max_depth"], depth)
        for name, value in node.get_xml_attrs().items():
            state["attributes"].append(name + "=" + value)
        if node.get_cdata().strip():
            state["text"].append(node.get_cdata().strip())
        if isinstance(node, jxmlease.XMLDictNode):
            for child in node.values():
                visit(child, depth + 1)

    visit(roots[0], 1)
    state["root"] = state["elements"][0]
    return state


def parse_xml(path):
    if os.path.getsize(path) > (1 << 20):
        return None
    return summarize(parse_tree(path))


def fuzz_one_input(data: bytes):
    with tempfile.NamedTemporaryFile(prefix="parsarium-jxmlease-", suffix=".xml") as source:
        source.write(data)
        source.flush()
        try:
            parse_xml(source.name)
        except PARSE_ERRORS:
            pass
