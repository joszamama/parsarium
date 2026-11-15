# PyQt6 — ASCII PNM / Python

- **Pinned release:** `6.12.0`
- **License:** GPL-3.0-only
- **Parsed scope:** P3 pixels
- **Underlying family:** Qt PPM image plugin
- **Local input API:** `PyQt6.QtGui.QImageReader(local path).read()`
- **Documentation:** [API reference](<https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtgui/qimagereader.html>)
- **Catalog evidence:** [parser record](../../../../data/python/ascii_pnm/parsers.json) · [control verification](../../../../data/python/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/python/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgb0": [
    255,
    0,
    0
  ],
  "rgb1": [
    0,
    255,
    0
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
