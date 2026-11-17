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

    def rgb(x: int) -> list[int]:
        pixel = image.pixelColor(x, 0)
        return [pixel.red(), pixel.green(), pixel.blue()]

    return {"width": image.width(), "height": image.height(),
            "rgb0": rgb(0), "rgb1": rgb(1)}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: adapter.py LOCAL_PNM_FILE")
    print(json.dumps(read_pnm(Path(sys.argv[1]))))
