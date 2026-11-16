"""Decode one local PNG through Pycairo's Cairo/libpng path."""

import sys

import cairo


if len(sys.argv) != 2:
    raise SystemExit("usage: run-once.py LOCAL_PNG_FILE")
surface = cairo.ImageSurface.create_from_png(sys.argv[1])
surface.flush()
raw = bytes(surface.get_data())
print(f"{surface.get_width()}x{surface.get_height()} first={raw[2]},{raw[1]},{raw[0]},{raw[3]}")
