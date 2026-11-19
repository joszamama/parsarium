"""Parse SVG dimensions and rectangle geometry from bytes."""

from io import BytesIO

from xml.etree.ElementTree import ParseError

from svgelements import SVG


def parse_svg(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    root = SVG.parse(BytesIO(data))
    observed = {}
    # svgelements leaves a dimension it cannot resolve to pixels (em, ex, %
    # without a context) as a Length or None; size is reported only when both
    # dimensions resolved to numbers.
    if all(isinstance(value, (int, float)) for value in (root.width, root.height)):
        observed["size"] = [int(root.width), int(root.height)]
    observed["rectangles"] = sum(type(element).__name__ == "Rect" for element in root.elements())
    return observed


def fuzz_one_input(data: bytes):
    try:
        parse_svg(data)
    except (ParseError, ValueError):
        pass
