"""Parse one local XML byte stream through Parsel's documented Selector(body=..., type="xml").

Selector strips the body and NUL bytes and calls lxml.etree.fromstring with
parsel.selector.SafeXMLParser(recover=True, resolve_entities=False, huge_tree=True,
encoding="utf-8"); libxml2 tokenizes the bytes. The summary reads the document
only through Selector.xpath(), get() and attrib, so names, namespaces and text come from
XPath over the tree Parsel built.
"""

from lxml import etree
from parsel import Selector


def value(selector, query):
    return selector.xpath(query).get()


def expanded(selector):
    uri = value(selector, "namespace-uri()")
    local = value(selector, "local-name()")
    return "{" + uri + "}" + local if uri else local


def in_scope(selector):
    # XPath namespace nodes: name() is the prefix ("" for the default namespace).
    count = int(float(value(selector, "count(namespace::*)")))
    pairs = {}
    for index in range(1, count + 1):
        prefix = value(selector, f"name(namespace::*[{index}])")
        if prefix != "xml":
            pairs[prefix] = value(selector, f"string(namespace::*[{index}])")
    return pairs


def parse_xml(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    document = Selector(body=data, type="xml")
    roots = document.xpath("/*")
    if not roots:
        return None
    state = {"attributes": [], "comments": [], "elements": [], "max_depth": 0,
             "namespace_declarations": 0, "namespaces": set(),
             "processing_instructions": [], "text": []}
    # In-scope namespaces of the open ancestors; //* is in document order, so the
    # parent is the latest element one level up.
    scopes = [{}]
    for element in document.xpath("//*"):
        state["elements"].append(expanded(element))
        depth = int(float(value(element, "count(ancestor-or-self::*)")))
        state["max_depth"] = max(state["max_depth"], depth)
        # A declaration is a change of the in-scope namespaces against the parent
        # element; xmlns="" shows up as the default prefix leaving scope.
        current = in_scope(element)
        inherited = scopes[depth - 1]
        del scopes[depth:]
        scopes.append(current)
        for prefix in current.keys() | inherited.keys():
            if current.get(prefix) != inherited.get(prefix):
                state["namespace_declarations"] += 1
                if current.get(prefix):
                    state["namespaces"].add(current[prefix])
        # Parsel turns attribute nodes into plain strings; Selector.attrib keeps
        # the {uri}local names in document order.
        for name, item in element.attrib.items():
            state["attributes"].append(name + "=" + item)
    state["text"] = [text.strip() for text in document.xpath("//text()").getall() if text.strip()]
    # lxml cannot use comment or PI nodes as an XPath context; read them by index.
    for index in range(1, int(float(value(document, "count(//comment())"))) + 1):
        state["comments"].append(value(document, f"string((//comment())[{index}])").strip())
    for index in range(1, int(float(value(document, "count(//processing-instruction())"))) + 1):
        target = value(document, f"name((//processing-instruction())[{index}])")
        body = value(document, f"string((//processing-instruction())[{index}])")
        state["processing_instructions"].append(target + " " + body if body else target)
    state["namespaces"] = sorted(state["namespaces"])
    state["root"] = expanded(roots[0])
    return state


def fuzz_one_input(data: bytes):
    try:
        parse_xml(data)
    except (etree.XMLSyntaxError, ValueError, UnicodeError):
        pass
