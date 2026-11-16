"""One input invokes the pinned pygame WAV parser."""

from adapter import parse_data
import pygame


def test_one_input(data: bytes) -> None:
    try:
        parse_data(data)
    except (pygame.error, ValueError, IndexError):
        return
