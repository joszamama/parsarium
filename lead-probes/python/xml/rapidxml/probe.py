"""Walk one valid XML control through RapidXml(bytes) with and without parse_cdata=True."""

import json
from pathlib import Path
import sys

import rapidxml


def show(value):
    # Guard only: the extension returns str, and raises (SystemError over UnicodeDecodeError)
    # when a stored value is not valid UTF-8.
    return value if isinstance(value, str) else "bytes:" + repr(value)


def walk(node, depth, state):
    for child in node.children:
        if child.name:
            state["elements"].append(child.name)
            state["max_depth"] = max(state["max_depth"], depth)
            for attribute in child.attributes:
                state["attributes"].append(show(attribute.name) + "=" + show(attribute.value))
            walk(child, depth + 1, state)
        elif show(child.value).strip() and depth > 1:
            state["text"].append(show(child.value).strip())


def run(data: bytes, parse_cdata: bool) -> dict:
    try:
        document = rapidxml.RapidXml(data, parse_cdata=parse_cdata) if parse_cdata else rapidxml.RapidXml(data)
        state = {"attributes": [], "elements": [], "max_depth": 0, "text": [], "element_values": []}
        walk(document, 1, state)

        def values(node):
            for child in node.children:
                if child.name:
                    if show(child.value).strip():
                        state["element_values"].append(show(child.name) + "=" + show(child.value).strip())
                    values(child)
        values(document)
        return {"ok": True, **state}
    except Exception as error:  # recorded, not hidden: the default route raises on the order control
        return {"ok": False, "error": f"{type(error).__name__}: {error}"[:300]}


data = Path(sys.argv[1]).read_bytes()
print(json.dumps({"default": run(data, False), "parse_cdata": run(data, True)}, ensure_ascii=False))
