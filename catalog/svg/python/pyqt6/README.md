# PyQt6 — SVG / Python

- **Pinned release:** `6.12.0`
- **License:** GPL-3.0-only
- **Parsed scope:** SVG rendering with dimensions and colored pixels
- **Underlying family:** QtSvg QSvgRenderer through PyQt6
- **Local input API:** `PyQt6.QtSvg.QSvgRenderer(local_svg_path)`
- **Documentation:** [API reference](<https://doc.qt.io/qt-6/qsvgrenderer.html>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/python/pyqt6/README.md)

```sh
python3 parsarium.py build svg python pyqt6
python3 parsarium.py run svg python pyqt6 controls/svg/red-green.svg
```
