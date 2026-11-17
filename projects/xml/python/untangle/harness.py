"""Parse one local XML file through the documented untangle.parse(path-like) API.

untangle 1.3.1 opens a path-like argument in binary mode and feeds it to
defusedxml.sax.make_parser(), a DefusedExpatParser over CPython's SAX Expat
driver. Its Handler builds Element objects from startElement/characters/
endElement events with namespace processing off, so element names are raw
qualified names with "-", "." and ":" replaced by "_" and xmlns declarations
stay ordinary attributes. The summary reads only the Element fields that
the handler filled in; it calls no Element methods.
"""

import os
from pathlib import Path
import tempfile
import xml.sax

from defusedxml.common import DefusedXmlException
import untangle

PARSE_ERRORS = (xml.sax.SAXException, DefusedXmlException, ValueError, UnicodeError)


def parse_tree(path):
    return untangle.parse(Path(path))


def summarize(document):
    if not document.children:
        return None
    root = document.children[0]
    state = {"attributes": [], "elements": [], "max_depth": 0,
             "namespace_declarations": 0, "namespaces": set(), "text": []}
    stack = [(root, 1)]
    while stack:
        element, depth = stack.pop()
        state["elements"].append(element._name)
        state["max_depth"] = max(state["max_depth"], depth)
        for name, value in element._attributes.items():
            if name == "xmlns" or name.startswith("xmlns:"):
                state["namespace_declarations"] += 1
                if value:
                    state["namespaces"].add(value)
            else:
                state["attributes"].append(name + "=" + value)
        if element.cdata.strip():
            state["text"].append(element.cdata.strip())
        stack.extend((child, depth + 1) for child in reversed(element.children))
    state["namespaces"] = sorted(state["namespaces"])
    state["root"] = root._name
    return state


def parse_xml(path):
    if os.path.getsize(path) > (1 << 20):
        return None
    return summarize(parse_tree(path))


def fuzz_one_input(data: bytes):
    # untangle documents path-like, filename, URL and XML-string input, not bytes;
    # byte inputs from queue replay go through a temporary path-like file.
    with tempfile.NamedTemporaryFile(prefix="parsarium-untangle-", suffix=".xml") as source:
        source.write(data)
        source.flush()
        try:
            parse_xml(source.name)
        except PARSE_ERRORS:
            pass
