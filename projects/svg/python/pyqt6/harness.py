"""Render one local SVG byte stream through PyQt6's QSvgRenderer (QtSvg 6.12.0)."""

from PyQt6.QtCore import QByteArray
from PyQt6.QtGui import QGuiApplication, QImage, QPainter
from PyQt6.QtSvg import QSvgRenderer

_APPLICATION = []


def parse_svg(data: bytes):
    if not data or len(data) > (1 << 20):
        return None
    # Qt requires a QGuiApplication before text is laid out (QFontDatabase);
    # without one, an SVG with <text> aborts the process. The image sets
    # QT_QPA_PLATFORM=offscreen.
    if QGuiApplication.instance() is None:
        _APPLICATION.append(QGuiApplication([]))
    renderer = QSvgRenderer(QByteArray(data))
    if not renderer.isValid():
        raise ValueError("QSvgRenderer rejected the SVG")
    size = renderer.defaultSize()
    if not (0 < size.width() <= 4096 and 0 < size.height() <= 4096):
        raise ValueError("SVG default size outside the harness bounds")
    image = QImage(size, QImage.Format.Format_ARGB32)
    image.fill(0)
    painter = QPainter(image)
    renderer.render(painter)
    painter.end()
    return {"size": [size.width(), size.height()],
            "red": list(image.pixelColor(0, 0).getRgb()),
            "green": list(image.pixelColor(min(1, size.width() - 1), 0).getRgb())}


def fuzz_one_input(data: bytes):
    try:
        parse_svg(data)
    except ValueError:
        pass
