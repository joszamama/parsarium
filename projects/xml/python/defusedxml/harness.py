"""Parse one local XML byte stream through the documented defusedxml.ElementTree.parse API.

defusedxml 0.7.1's parse() builds a DefusedXMLParser (a subclass of CPython's
pure-Python xml.etree.ElementTree.XMLParser, loaded with _elementtree blocked)
with the default C TreeBuilder target, installs its entity and external
reference guards on the pyexpat parser and hands the stream to
ElementTree.parse; Expat does the XML parsing. The summary reads the finished
namespace-expanded ElementTree. ElementTree keeps no xmlns declarations, so
"namespaces" lists the URIs carried by expanded element and attribute names.
"""

from io import BytesIO
from xml.etree.ElementTree import ParseError

from defusedxml.common import DefusedXmlException
import defusedxml.ElementTree

PARSE_ERRORS = (ParseError, DefusedXmlException, ValueError, UnicodeError)


def parse_tree(data: bytes):
    return defusedxml.ElementTree.parse(BytesIO(data))


def summarize(tree):
    root = tree.getroot()
    state = {"attributes": [], "elements": [], "max_depth": 0, "namespaces": set(), "text": []}

    def uri(name):
        if name.startswith("{"):
            state["namespaces"].add(name[1:].partition("}")[0])

    def append_text(value):
        if value and value.strip():
            state["text"].append(value.strip())

    def walk(element, depth):
        state["elements"].append(element.tag)
        uri(element.tag)
        state["max_depth"] = max(state["max_depth"], depth)
        for name, value in element.attrib.items():
            uri(name)
            state["attributes"].append(name + "=" + value)
        append_text(element.text)
        for child in element:
            walk(child, depth + 1)
            append_text(child.tail)

    walk(root, 1)
    state["namespaces"] = sorted(state["namespaces"])
    state["root"] = root.tag
    return state


def parse_xml(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    return summarize(parse_tree(data))


def fuzz_one_input(data: bytes):
    try:
        parse_xml(data)
    except PARSE_ERRORS:
        pass
