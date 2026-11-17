"""Parse one local XML byte stream through pyquery's documented PyQuery(bytes, parser="xml").

pyquery.pyquery.fromstring maps parser="xml" to lxml.etree.fromstring with lxml's
default XMLParser; libxml2 tokenizes the bytes. The summary walks the document
with PyQuery.contents() (child text nodes and child elements, as returned by
pyquery) from the root PyQuery object. A PyQuery object is a list of lxml
elements, so element names, attributes and in-scope namespaces are read from
those returned elements (tag, attrib, nsmap). Comments and processing
instructions are not returned by contents(), so they are not in the summary.
"""

from lxml import etree
from pyquery import PyQuery


def parse_xml(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    document = PyQuery(data, parser="xml")
    if len(document) != 1:
        return None
    state = {"attributes": [], "elements": [], "max_depth": 0,
             "namespace_declarations": 0, "namespaces": set(), "text": []}
    pending = []

    def flush():
        text = "".join(pending).strip()
        if text:
            state["text"].append(text)
        pending.clear()

    def visit(element, depth, inherited):
        flush()
        state["elements"].append(element.tag)
        state["max_depth"] = max(state["max_depth"], depth)
        current = dict(element.nsmap)
        # A declaration is a change of the in-scope namespaces against the parent
        # element; xmlns="" shows up as the default prefix leaving scope.
        for prefix in current.keys() | inherited.keys():
            if current.get(prefix) != inherited.get(prefix):
                state["namespace_declarations"] += 1
                if current.get(prefix):
                    state["namespaces"].add(current[prefix])
        for name, value in element.attrib.items():
            state["attributes"].append(name + "=" + value)
        for item in PyQuery(element).contents():
            if isinstance(item, str):
                pending.append(item)
            else:
                visit(item, depth + 1, current)
        flush()

    visit(document[0], 1, {})
    state["namespaces"] = sorted(state["namespaces"])
    state["root"] = state["elements"][0]
    return state


def fuzz_one_input(data: bytes):
    try:
        parse_xml(data)
    except (etree.XMLSyntaxError, ValueError, UnicodeError):
        pass
