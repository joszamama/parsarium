"""Byte-input PyPNG harness shared by coverage replay and Atheris."""

import png


def parse_png(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    width, height, rows, _ = png.Reader(bytes=data).asRGBA8()
    if width <= 0 or height <= 0 or width > 2048 or height > 2048:
        return None
    first = second = None
    count = 0
    for row in rows:
        if len(row) != width * 4:
            return None
        if count == 0:
            first = list(row[:4])
            second = list(row[4:8]) if width > 1 else None
        count += 1
    if count != height:
        return None
    return {"width": width, "height": height, "rgba0": first, "rgba1": second}


def fuzz_one_input(data: bytes):
    try:
        parse_png(data)
    except (png.Error, EOFError, ValueError):
        pass
