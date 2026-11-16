"""Decode ASCII PNM bytes with pygame's SDL image loader."""

from io import BytesIO


def parse_data(data: bytes) -> dict:
    import pygame

    image = pygame.image.load(BytesIO(data), "control.ppm")
    first = image.get_at((0, 0))
    second = image.get_at((1, 0))
    return {
        "width": image.get_width(),
        "height": image.get_height(),
        "rgb0": [first.r, first.g, first.b],
        "rgb1": [second.r, second.g, second.b],
    }
