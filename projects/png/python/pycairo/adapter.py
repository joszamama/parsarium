"""Decode PNG bytes through the pinned Pycairo/Cairo PNG loader."""

from io import BytesIO


def parse_data(data: bytes) -> dict:
    import cairo

    surface = cairo.ImageSurface.create_from_png(BytesIO(data))
    surface.flush()
    raw = bytes(surface.get_data())
    if surface.get_width() < 2 or surface.get_height() < 1:
        raise ValueError("need two pixels for the observed result")

    def rgba(offset):
        return [raw[offset + 2], raw[offset + 1], raw[offset], raw[offset + 3]]

    return {
        "width": surface.get_width(),
        "height": surface.get_height(),
        "rgba0": rgba(0),
        "rgba1": rgba(4),
    }
