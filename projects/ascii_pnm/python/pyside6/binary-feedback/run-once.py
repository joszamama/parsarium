"""Read one local PNM file through Qt's byte-stream image reader."""
import sys
from pathlib import Path

from PySide6.QtCore import QBuffer, QByteArray, QIODevice
from PySide6.QtGui import QImageReader


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit('usage: run-once.py LOCAL_PNM_FILE')
    data = Path(sys.argv[1]).read_bytes()
    source = QBuffer()
    source.setData(QByteArray(data))
    if not source.open(QIODevice.OpenModeFlag.ReadOnly):
        raise SystemExit('failed to open byte buffer')
    reader = QImageReader(source)
    reader.setDecideFormatFromContent(True)
    image = reader.read()
    if image.isNull():
        raise SystemExit(reader.errorString())
    color = image.pixelColor(0, 0)
    print(f'{image.width()}x{image.height()} first={color.red()},{color.green()},{color.blue()}')


if __name__ == '__main__':
    main()
