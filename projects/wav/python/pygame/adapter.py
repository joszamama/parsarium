"""Decode WAV bytes through pygame's SDL mixer loader."""

from io import BytesIO
import struct


def parse_data(data: bytes) -> dict:
    import pygame

    if pygame.mixer.get_init() is None:
        pygame.mixer.init(frequency=8000, size=-16, channels=1, allowedchanges=0)
    sound = pygame.mixer.Sound(file=BytesIO(data))
    raw = sound.get_raw()
    if len(raw) != 8:
        raise ValueError(f"unexpected decoded sample count: {len(raw) // 2}")
    frequency, _, channels = pygame.mixer.get_init()
    return {
        "sample_rate": frequency,
        "channels": channels,
        "samples": list(struct.unpack("<4h", raw)),
    }
