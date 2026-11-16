"""Decode one local WAV file with pygame's SDL mixer loader."""

import sys

import pygame


if len(sys.argv) != 2:
    raise SystemExit("usage: run-once.py LOCAL_WAV_FILE")
pygame.mixer.init(frequency=8000, size=-16, channels=1, allowedchanges=0)
sound = pygame.mixer.Sound(sys.argv[1])
frequency, _, channels = pygame.mixer.get_init()
print(f"{frequency}Hz/{channels}ch samples={len(sound.get_raw()) // 2}")
