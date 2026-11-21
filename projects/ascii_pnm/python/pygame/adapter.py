"""Decode ASCII PNM bytes with pygame's SDL image loader."""

from io import BytesIO


def parse_data(data: bytes) -> dict:
    import pygame

    image = pygame.image.load(BytesIO(data), "control.ppm")
    width, height = image.get_width(), image.get_height()
    first = image.get_at((0, 0))
    # The second pixel is the next one in raster order, if the image has one.
    at = (1, 0) if width > 1 else (0, 1) if height > 1 else None
    second = None if at is None else image.get_at(at)
    return {
        "width": width,
        "height": height,
        "rgb0": [first.r, first.g, first.b],
        "rgb1": None if second is None else [second.r, second.g, second.b],
    }
