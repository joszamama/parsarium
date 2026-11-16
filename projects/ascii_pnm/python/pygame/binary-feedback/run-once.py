"""Decode one local PNM file with pygame's SDL image loader."""

import sys

import pygame


if len(sys.argv) != 2:
    raise SystemExit("usage: run-once.py LOCAL_PNM_FILE")
image = pygame.image.load(sys.argv[1])
color = image.get_at((0, 0))
print(f"{image.get_width()}x{image.get_height()} first={color.r},{color.g},{color.b}")
