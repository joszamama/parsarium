"""Decode ASCII P3 PNM pixels from bytes using netpbmfile."""

from io import BytesIO

from netpbmfile import NetpbmFile


def parse_ascii_pnm(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    with NetpbmFile(BytesIO(data)) as image:
        if image.magicnumber != "P3":
            return None
        pixels = image.asarray()
    if (pixels.ndim != 3 or pixels.shape[2] != 3
            or pixels.shape[0] < 1 or pixels.shape[1] < 1):
        return None
    return {"width": int(pixels.shape[1]), "height": int(pixels.shape[0]),
            "rgb0": [int(value) for value in pixels[0, 0]],
            "rgb1": [int(value) for value in pixels[0, 1]] if pixels.shape[1] > 1 else None}


def fuzz_one_input(data: bytes):
    try:
        parse_ascii_pnm(data)
    except ValueError:
        pass
