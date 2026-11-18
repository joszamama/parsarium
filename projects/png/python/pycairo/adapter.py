"""Decode PNG bytes through the pinned Pycairo/Cairo PNG loader."""

from io import BytesIO
import struct


def _float_byte(value: float) -> int:
    # Cairo stores 16-bit PNG samples as value / 65535; report the high byte.
    if not value > 0.0:
        return 0
    if value >= 1.0:
        return 255
    return int(value * 65535.0 + 0.5) >> 8


def _unpremultiply(color: int, alpha: int) -> int:
    # ARGB32 colour is premultiplied by alpha; report straight RGBA, rounded.
    # Fully transparent pixels keep the stored 0,0,0,0.
    if alpha in (0, 255):
        return color
    return min(255, (color * 510 + alpha) // (2 * alpha))


def parse_data(data: bytes) -> dict:
    import cairo

    surface = cairo.ImageSurface.create_from_png(BytesIO(data))
    surface.flush()
    raw = bytes(surface.get_data())
    image_format = surface.get_format()
    width = surface.get_width()

    def rgba(x):
        if image_format in (cairo.Format.RGBA128F, cairo.Format.RGB96F):
            bands = 4 if image_format == cairo.Format.RGBA128F else 3
            values = list(struct.unpack_from(f"={bands}f", raw, x * bands * 4)) + [1.0] * (4 - bands)
            # RGBA128F colour is premultiplied by alpha; RGB96F has no alpha.
            if image_format == cairo.Format.RGBA128F and values[3] > 0.0:
                values[:3] = [value / values[3] for value in values[:3]]
            return [_float_byte(value) for value in values]
        (value,) = struct.unpack_from("=I", raw, x * 4)
        alpha = value >> 24 if image_format == cairo.Format.ARGB32 else 255
        return [_unpremultiply((value >> shift) & 255, alpha) for shift in (16, 8, 0)] + [alpha]

    result = {
        "width": width,
        "height": surface.get_height(),
        "rgba0": rgba(0),
    }
    if width > 1:
        result["rgba1"] = rgba(1)
    return result
