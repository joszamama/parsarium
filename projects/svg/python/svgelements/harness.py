"""Parse SVG dimensions and rectangle geometry from bytes."""

from io import BytesIO

from xml.etree.ElementTree import ParseError

from svgelements import SVG


def parse_svg(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    root = SVG.parse(BytesIO(data))
    if root.width is None or root.height is None:
        return None
    return {"size": [int(root.width), int(root.height)],
            "rectangles": sum(type(element).__name__ == "Rect" for element in root.elements())}


def fuzz_one_input(data: bytes):
    try:
        parse_svg(data)
    except (ParseError, ValueError):
        pass
