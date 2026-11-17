"""Decode an ID3v2-tagged MP3 through pygame's SDL mixer loader."""

import tempfile


def parse_data(data: bytes) -> dict:
    import pygame

    if pygame.mixer.get_init() is None:
        pygame.mixer.init(frequency=8000, size=-16, channels=1, allowedchanges=0)
    with tempfile.NamedTemporaryFile(suffix=".mp3") as source:
        source.write(data)
        source.flush()
        sound = pygame.mixer.Sound(source.name)
        return {"duration_ms": round(sound.get_length() * 1000)}
