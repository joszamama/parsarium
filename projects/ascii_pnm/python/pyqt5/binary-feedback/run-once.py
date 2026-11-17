"""Read one local PNM path through the Qt image reader for AFL++ QEMU."""

import sys
from PyQt5.QtGui import QImageReader


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: run-once.py LOCAL_PNM_FILE")
    reader = QImageReader(sys.argv[1])
    image = reader.read()
    if image.isNull():
        raise SystemExit(reader.errorString())
    color = image.pixelColor(0, 0)
    print(f"{image.width()}x{image.height()} first={color.red()},{color.green()},{color.blue()}")


if __name__ == "__main__":
    main()
