"""Decode a local ASCII PNM file with the pinned PyQt5 QImageReader API."""

import json
import sys
from pathlib import Path

def read_pnm(path: Path) -> dict:
    from PyQt5.QtGui import QImageReader
    reader = QImageReader(str(path))
    image = reader.read()
    if image.isNull():
        raise ValueError(f"Qt could not read the PNM: {reader.errorString()}")

    def rgb(x: int, y: int) -> list[int]:
        pixel = image.pixelColor(x, y)
        return [pixel.red(), pixel.green(), pixel.blue()]

    # The second pixel is the next one in raster order, if the image has one.
    width, height = image.width(), image.height()
    second = rgb(1, 0) if width > 1 else rgb(0, 1) if height > 1 else None
    return {"width": width, "height": height, "rgb0": rgb(0, 0), "rgb1": second}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: adapter.py LOCAL_PNM_FILE")
    print(json.dumps(read_pnm(Path(sys.argv[1]))))
