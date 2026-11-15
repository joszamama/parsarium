# PySide6 — SVG / Python

- **Pinned release:** `6.12.0`
- **License:** LGPL-3.0-only OR GPL-2.0-only OR GPL-3.0-only
- **Parsed scope:** SVG rendering with dimensions and colored pixels
- **Underlying family:** QtSvg QSvgRenderer through PySide6
- **Local input API:** `PySide6.QtSvg.QSvgRenderer(local_svg_path)`
- **Documentation:** [API reference](<https://doc.qt.io/qtforpython-6/PySide6/QtSvg/QSvgRenderer.html>)
- **Catalog evidence:** [parser record](../../../../data/python/svg/parsers.json) · [control verification](../../../../data/python/svg/verification.json) · [within-ecosystem ranking](../../../../data/python/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "size": [
    2,
    1
  ],
  "red": [
    255,
    0,
    0,
    255
  ],
  "green": [
    0,
    255,
    0,
    255
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
