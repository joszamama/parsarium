"""Load one local XML byte stream through the documented xmlschema.XMLResource API.

xmlschema 4.3.2's XMLResource(BytesIO(data)) keeps the stream in memory (a
BytesIO source is never treated as a URL or file path and, with the default
defuse='remote', is not pre-scanned) and XMLResourceLoader._parse drives
xml.etree.ElementTree.iterparse with start-ns/end-ns/start/end/comment/pi
events. Expat tokenizes, CPython's C _elementtree XMLParser and TreeBuilder
build the namespace-expanded tree, and xmlschema's loop records each element's
in-scope namespace map and its own xmlns declarations. The summary reads the
finished resource: the tree from XMLResource.root and the declarations from
XMLResource.get_xmlns.
"""

from io import BytesIO
from xml.etree.ElementTree import ParseError

from xmlschema import XMLResource
from xmlschema.exceptions import XMLSchemaException

PARSE_ERRORS = (ParseError, XMLSchemaException, ValueError, UnicodeError)


def parse_resource(data: bytes):
    return XMLResource(BytesIO(data))


def summarize(resource):
    state = {"attributes": [], "elements": [], "max_depth": 0,
             "namespace_declarations": 0, "namespaces": set(), "text": []}

    def append_text(value):
        if value and value.strip():
            state["text"].append(value.strip())

    def walk(element, depth):
        state["elements"].append(element.tag)
        state["max_depth"] = max(state["max_depth"], depth)
        for _prefix, uri in resource.get_xmlns(element) or ():
            state["namespace_declarations"] += 1
            if uri:
                state["namespaces"].add(uri)
        for name, value in element.attrib.items():
            state["attributes"].append(name + "=" + value)
        append_text(element.text)
        for child in element:
            if isinstance(child.tag, str):
                walk(child, depth + 1)
            append_text(child.tail)

    walk(resource.root, 1)
    state["namespaces"] = sorted(state["namespaces"])
    state["root"] = resource.root.tag
    return state


def parse_xml(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    return summarize(parse_resource(data))


def fuzz_one_input(data: bytes):
    try:
        parse_xml(data)
    except PARSE_ERRORS:
        pass
