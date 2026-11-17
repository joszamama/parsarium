"""Decode one local ID3v2-tagged MP3 through pygame's SDL mixer loader."""

import sys

import pygame


if len(sys.argv) != 2:
    raise SystemExit("usage: run-once.py LOCAL_MP3_FILE")
pygame.mixer.init(frequency=8000, size=-16, channels=1, allowedchanges=0)
sound = pygame.mixer.Sound(sys.argv[1])
print(f"duration_ms={round(sound.get_length() * 1000)}")
