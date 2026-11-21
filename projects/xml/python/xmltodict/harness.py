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
    # Every child element of the root is counted, whatever its name. xmltodict groups children by
    # name in first-appearance order, so the first group's first value is the first child; the
    # second child is known when there is one name, or when the first name occurs once. Otherwise
    # (a, a, b and a, b, a give the same dict) xmltodict does not keep it and it is not reported.
    groups = [value if isinstance(value, list) else [value]
              for key, value in root_value.items() if not key.startswith(("@", "#"))]
    result["child_count"] = sum(len(group) for group in groups)
    if groups:
        result["first_item_id"], result["first_item_text"] = child_fields(groups[0][0])
    if len(groups[0] if groups else []) > 1 and len(groups) == 1:
        result["second_item_text"] = child_fields(groups[0][1])[1]
    elif len(groups) > 1 and len(groups[0]) == 1:
        result["second_item_text"] = child_fields(groups[1][0])[1]
    return result


def child_fields(value):
    """(@id, #text) of one child as xmltodict returns it: a dict, a text-only string, or None."""
    if isinstance(value, dict):
        return value.get("@id"), value.get("#text")
    return None, value


def fuzz_one_input(data: bytes):
    try:
        parse_xml(data)
    except (ExpatError, ValueError, UnicodeError, TypeError):
        pass
