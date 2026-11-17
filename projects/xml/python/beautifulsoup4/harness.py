"""Parse one local XML byte stream through Beautiful Soup's documented "xml" builder.

BeautifulSoup(bytes, "xml") selects bs4.builder.LXMLTreeBuilderForXML, which feeds
the bytes to lxml.etree.XMLParser(target=builder, recover=True) and builds the bs4
tree from lxml's start/end/data/comment/pi callbacks. The summary reads only the
resulting bs4 tree.
"""

from bs4 import BeautifulSoup, Tag
from bs4.builder import ParserRejectedMarkup
from bs4.element import Comment, ProcessingInstruction

XMLNS = "http://www.w3.org/2000/xmlns/"


def expanded(namespace, name):
    return "{" + namespace + "}" + name if namespace else name


def parse_xml(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    soup = BeautifulSoup(data, "xml")
    root = next((child for child in soup.children if isinstance(child, Tag)), None)
    if root is None:
        return None
    state = {"attributes": [], "comments": [], "elements": [], "max_depth": 0,
             "namespace_declarations": 0, "namespaces": set(),
             "processing_instructions": [], "text": []}

    def visit(node, depth):
        for child in node.children:
            if isinstance(child, Tag):
                walk(child, depth + 1)
            elif isinstance(child, Comment):
                state["comments"].append(str(child).strip())
            elif isinstance(child, ProcessingInstruction):
                state["processing_instructions"].append(str(child))
            elif child.strip():
                state["text"].append(child.strip())

    def walk(tag, depth):
        state["elements"].append(expanded(tag.namespace, tag.name))
        state["max_depth"] = max(state["max_depth"], depth)
        for name, value in tag.attrs.items():
            # bs4 keeps lxml's new namespace declarations as xmlns attributes.
            if getattr(name, "namespace", None) == XMLNS:
                state["namespace_declarations"] += 1
                if value:
                    state["namespaces"].add(value)
            else:
                state["attributes"].append(
                    expanded(getattr(name, "namespace", None), getattr(name, "name", None) or name)
                    + "=" + value)
        visit(tag, depth)

    visit(soup, 0)
    state["namespaces"] = sorted(state["namespaces"])
    state["root"] = expanded(root.namespace, root.name)
    return state


def fuzz_one_input(data: bytes):
    try:
        parse_xml(data)
    except (ParserRejectedMarkup, ValueError, UnicodeError):
        pass
