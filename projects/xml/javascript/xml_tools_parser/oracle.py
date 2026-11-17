"""Independent Expat check for the raw QName hierarchy in the two XML controls.

Expat is intentionally configured without namespace expansion. This oracle
does not certify the CST parser's namespace resolution or entity decoding.
"""

import json
import sys
from xml.parsers import expat


def structure(data: bytes) -> dict:
    parser = expat.ParserCreate()
    parser.ordered_attributes = True
    roots: list[dict] = []
    stack: list[dict] = []
    max_depth = 0

    def start(name: str, attributes: list[str]) -> None:
        nonlocal max_depth
        node = {"qname": name,
                "attributes": [attributes[index] for index in range(0, len(attributes), 2)],
                "children": []}
        if stack:
            stack[-1]["children"].append(node)
        else:
            roots.append(node)
        stack.append(node)
        max_depth = max(max_depth, len(stack))

    def end(_name: str) -> None:
        stack.pop()

    parser.StartElementHandler = start
    parser.EndElementHandler = end
    parser.Parse(data, True)
    if len(roots) != 1:
        raise ValueError(f"expected one root, got {len(roots)}")
    return {"tree": roots[0], "max_depth": max_depth}


if __name__ == "__main__":
    for path in sys.argv[1:]:
        with open(path, "rb") as source:
            print(json.dumps(structure(source.read()), ensure_ascii=False, sort_keys=True))
