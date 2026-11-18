# qtsvg — SVG / C++

- **Pinned release:** `6.12.0`
- **Upstream:** [source repository](<https://code.qt.io/cgit/qt/qtsvg.git/>) · [Debian](<https://tracker.debian.org/pkg/qtsvg-opensource-src>)
- **License:** LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
- **Parsed scope:** parsed SVG dimensions and rendered red/green rectangle pixels
- **Underlying family:** QtSvg QSvgRenderer document parser and Qt painter
- **Local input API:** `QSvgRenderer(QString local filename) or QSvgRenderer::load(QByteArray local bytes); isValid; defaultSize; render(QPainter*) to QImage`
- **Documentation:** [API reference](<https://doc.qt.io/qt-6/qsvgrenderer.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/svg/parsers.json) · [control verification](../../../../data/cpp/svg/verification.json) · [within-ecosystem ranking](../../../../data/cpp/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "first": [
    255,
    0,
    0
  ],
  "second": [
    0,
    255,
    0
  ]
}
```

QtSvg provides its own C++ SVG document reader. QtCore and QtGui supply the paint device and pixels; this row does not re-count a second QtSvg API as an independent parser.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/cpp/qtsvg/README.md)

```sh
python3 parsarium.py build svg cpp qtsvg
python3 parsarium.py run svg cpp qtsvg controls/svg/red-green.svg
```
