"""Parse a complete local XML byte stream through CPython ElementTree."""

from io import BytesIO
import xml.etree.ElementTree as ET


def parse_xml(data: bytes):
    if len(data) > (1 << 20):
        return None
    root = ET.parse(BytesIO(data)).getroot()
    namespace = None
    local_name = root.tag
    if root.tag.startswith("{"):
        namespace, local_name = root.tag[1:].split("}", 1)
    children = list(root)
    result = {"root": local_name, "namespace": namespace,
              "child_count": len(children)}
    if children:
        result["first_item_id"] = children[0].get("id")
        result["first_item_text"] = children[0].text
    if len(children) > 1:
        result["second_item_text"] = children[1].text
    return result


def fuzz_one_input(data: bytes):
    try:
        parse_xml(data)
    except (ET.ParseError, ValueError, UnicodeError, TypeError):
        pass
