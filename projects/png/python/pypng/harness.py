"""Byte-input PyPNG harness shared by coverage replay and Atheris."""

import png


def parse_png(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    width, height, rows, _ = png.Reader(bytes=data).asRGBA8()
    first = second = None
    count = 0
    for row in rows:
        if len(row) != width * 4:
            return None
        if count == 0:
            first = list(row[:4])
            second = list(row[4:8])
        count += 1
    if count != height:
        return None
    result = {"width": width, "height": height, "rgba0": first}
    if width > 1:
        result["rgba1"] = second
    return result


def fuzz_one_input(data: bytes):
    try:
        parse_png(data)
    except (png.Error, EOFError, ValueError):
        pass
