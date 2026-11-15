# qtsvg — SVG / C++

- **Pinned release:** `6.12.0`
- **License:** LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
- **Parsed scope:** parsed SVG dimensions and rendered red/green rectangle pixels
- **Underlying family:** QtSvg QSvgRenderer document parser and Qt painter
- **Local input API:** `QSvgRenderer(QString local filename); isValid; defaultSize; render(QPainter*) to QImage`
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
