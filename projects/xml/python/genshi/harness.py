"""Parse one local XML file through Genshi's documented genshi.input.XMLParser API.

Genshi 0.7.12's XMLParser(source) creates a CPython pyexpat parser in
namespace mode (ParserCreate(encoding, '}')) and turns its callbacks into
Genshi markup-stream events: START (QName tag, Attrs), END, TEXT, START_NS
(prefix, uri), END_NS, START_CDATA/END_CDATA, COMMENT, PI and XML_DECL.
Element and attribute QNames carry the namespace URI Expat resolved, and
each xmlns/xmlns:* declaration arrives as a START_NS event. The summary only
formats these events: expanded {uri}local names, attributes sorted per
element (as in the other namespace-aware XML paths), the declaration count,
the distinct non-empty URIs the declarations bind, the maximum depth and the
trimmed, non-empty character-data runs between markup events.
"""

from io import BytesIO
import os
from pathlib import Path
from xml.parsers import expat

from genshi.core import COMMENT, END, PI, START, START_NS, TEXT
from genshi.input import ParseError, XMLParser

PARSE_ERRORS = (ParseError, expat.ExpatError, ValueError, UnicodeError)


def parse_tree(path):
    # Iterating the parser runs Expat and Genshi's event handlers to the end.
    return list(XMLParser(BytesIO(Path(path).read_bytes()), filename=os.path.basename(path)))


def expanded(qname):
    return "{%s}%s" % (qname.namespace, qname.localname) if qname.namespace else qname.localname


def summarize(events):
    state = {"attributes": [], "elements": [], "max_depth": 0, "namespace_declarations": 0, "text": []}
    namespaces, run, depth = set(), [], 0

    def flush():
        value = "".join(run).strip()
        if value:
            state["text"].append(value)
        run.clear()

    for kind, data, _ in events:
        if kind == START:
            flush()
            tag, attrs = data
            depth += 1
            state["max_depth"] = max(state["max_depth"], depth)
            state["elements"].append(expanded(tag))
            state["attributes"].extend(sorted(expanded(name) + "=" + value for name, value in attrs))
        elif kind == END:
            flush()
            depth -= 1
        elif kind == TEXT:
            run.append(data)
        elif kind == START_NS:
            state["namespace_declarations"] += 1
            if data[1]:
                namespaces.add(data[1])
        elif kind in (COMMENT, PI):
            flush()
    flush()
    if not state["elements"]:
        return None
    state["namespaces"] = sorted(namespaces)
    state["root"] = state["elements"][0]
    return state


def parse_xml(path):
    if os.path.getsize(path) > (1 << 20):
        return None
    return summarize(parse_tree(path))


def fuzz_one_input(data: bytes):
    import tempfile
    with tempfile.NamedTemporaryFile(prefix="parsarium-genshi-", suffix=".xml") as source:
        source.write(data)
        source.flush()
        try:
            parse_xml(source.name)
        except PARSE_ERRORS:
            pass
