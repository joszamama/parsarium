# qtbase — ASCII PNM / C++

- **Pinned release:** `6.12.0`
- **License:** LGPL-3.0-only
- **Parsed scope:** P3 dimensions and two decoded RGBA pixels
- **Underlying family:** QtBase native QPPMHandler
- **Local input API:** `QImageReader(localPath, "ppm").read(); QImage::pixelColor(x,y)`
- **Documentation:** [API reference](<https://doc.qt.io/qt-6/qimagereader.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_pnm/parsers.json) · [control verification](../../../../data/cpp/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "first": [
    255,
    0,
    0,
    255
  ],
  "second": [
    0,
    255,
    0,
    255
  ]
}
```

QtBase QImageReader delegates PPM to its built-in qppmhandler; installed QtGui and QtCore frameworks are pinned by SHA-256. QtBase covers many unrelated GUI APIs, so repository stars are a broad adoption proxy.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/cpp/qtbase/README.md)

```sh
python3 parsarium.py build ascii_pnm cpp qtbase
python3 parsarium.py run ascii_pnm cpp qtbase controls/ascii_pnm/red-green.ppm
```
