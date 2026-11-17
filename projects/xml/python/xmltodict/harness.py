"""Parse a complete local XML byte stream through xmltodict and Expat."""

from io import BytesIO
from xml.parsers.expat import ExpatError

import xmltodict


def parse_xml(data: bytes):
    if len(data) > (1 << 20):
        return None
    document = xmltodict.parse(BytesIO(data), process_namespaces=True,
                               namespace_separator="|", disable_entities=True)
    root_name, root_value = next(iter(document.items()))
    namespace, _, local_name = root_name.rpartition("|")
    if not local_name:
        local_name = root_name
    result = {"root": local_name, "namespace": namespace or None}
    if not isinstance(root_value, dict):
        result["child_count"] = 0
        return result
    child_name = namespace + "|item" if namespace else "item"
    items = root_value.get(child_name, [])
    if isinstance(items, dict):
        items = [items]
    result["child_count"] = len(items)
    if items and isinstance(items[0], dict):
        result["first_item_id"] = items[0].get("@id")
        result["first_item_text"] = items[0].get("#text")
    if len(items) > 1 and isinstance(items[1], dict):
        result["second_item_text"] = items[1].get("#text")
    return result


def fuzz_one_input(data: bytes):
    try:
        parse_xml(data)
    except (ExpatError, ValueError, UnicodeError, TypeError):
        pass
