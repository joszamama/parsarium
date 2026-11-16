"""Render a local SVG file with the pinned PyQt6 QSvgRenderer API."""

import json
import os
import sys
from pathlib import Path

# Offscreen GUI context so QtSvg text/font paths never abort without a display.
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
# Deterministic QHash probing keeps QtSvg binary feedback repeatable.
os.environ.setdefault("QT_HASH_SEED", "0")

_application = None


def gui_application():
    global _application
    from PyQt6.QtGui import QGuiApplication
    if QGuiApplication.instance() is None:
        _application = QGuiApplication(["parsarium-pyqt6-svg"])
    return QGuiApplication.instance()


def render_svg(path: Path) -> dict:
    gui_application()
    from PyQt6.QtGui import QImage, QPainter
    from PyQt6.QtSvg import QSvgRenderer
    renderer = QSvgRenderer(str(path))
    if not renderer.isValid():
        raise ValueError("QSvgRenderer rejected the SVG")
    size = renderer.defaultSize()
    if size.isEmpty() or size.width() * size.height() > (1 << 24):
        raise ValueError(f"unsupported SVG size: {size.width()}x{size.height()}")
    image = QImage(size, QImage.Format.Format_ARGB32)
    image.fill(0)
    painter = QPainter(image)
    renderer.render(painter)
    painter.end()
    return {"size": [size.width(), size.height()],
            "red": list(image.pixelColor(0, 0).getRgb()),
            "green": list(image.pixelColor(1, 0).getRgb()) if size.width() > 1 else None}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("usage: adapter.py LOCAL_SVG_FILE")
    print(json.dumps(render_svg(Path(sys.argv[1])), sort_keys=True))
