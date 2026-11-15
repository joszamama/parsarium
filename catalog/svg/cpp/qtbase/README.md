# qtbase — SVG / C++

- **Pinned release:** `6.12.0`
- **License:** LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
- **Parsed scope:** parsed SVG dimensions and rendered red/green rectangle pixels
- **Underlying family:** QtBase QImageReader with QtSvg image plugin
- **Local input API:** `QImageReader(QString local SVG filename, "svg"); read() to QImage; pixelColor`
- **Documentation:** [API reference](<https://doc.qt.io/qt-6/qimagereader.html>)
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

QtBase provides the generic image input API; the hash-pinned QtSvg plugin and framework perform SVG syntax parsing. This shares the QtSvg engine with the separately verified QSvgRenderer package path.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
