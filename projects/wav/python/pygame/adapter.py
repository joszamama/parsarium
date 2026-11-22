"""Decode WAV bytes through pygame's SDL mixer loader."""

from io import BytesIO
import struct


def parse_data(data: bytes) -> dict:
    import pygame

    if pygame.mixer.get_init() is None:
        pygame.mixer.init(frequency=8000, size=-16, channels=1, allowedchanges=0)
    sound = pygame.mixer.Sound(file=BytesIO(data))
    # Sound converts the decoded audio to the mixer format opened above, so
    # sample_rate and channels are the mixer's and the samples are the first
    # (at most four) samples of the converted audio.
    raw = sound.get_raw()
    frequency, _, channels = pygame.mixer.get_init()
    count = min(4, len(raw) // 2)
    return {
        "sample_rate": frequency,
        "channels": channels,
        "samples": list(struct.unpack(f"<{count}h", raw[:2 * count])),
    }
