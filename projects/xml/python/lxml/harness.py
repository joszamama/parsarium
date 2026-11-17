"""Parse one local XML byte stream through lxml's libxml2-backed XML parser."""

from io import BytesIO

from lxml import etree


def parse_xml(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    parser = etree.XMLParser(resolve_entities=False, no_network=True, recover=False)
    root = etree.parse(BytesIO(data), parser).getroot()
    state = {"attributes": [], "elements": [], "max_depth": 0,
             "namespace_declarations": 0, "namespaces": set(), "text": []}

    def append_text(value):
        if value and value.strip():
            state["text"].append(value.strip())

    def walk(element, depth, inherited):
        state["elements"].append(element.tag)
        state["max_depth"] = max(state["max_depth"], depth)
        current = element.nsmap
        for prefix, uri in current.items():
            if inherited.get(prefix) != uri:
                state["namespace_declarations"] += 1
                if uri:
                    state["namespaces"].add(uri)
        for name, value in element.attrib.items():
            state["attributes"].append(name + "=" + value)
        append_text(element.text)
        for child in element:
            if isinstance(child.tag, str):
                walk(child, depth + 1, current)
            append_text(child.tail)

    walk(root, 1, {})
    state["namespaces"] = sorted(state["namespaces"])
    state["root"] = root.tag
    return state


def fuzz_one_input(data: bytes):
    try:
        parse_xml(data)
    except (etree.XMLSyntaxError, ValueError, UnicodeError):
        pass
