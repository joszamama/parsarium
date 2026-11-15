# wxPython — ASCII PNM / Python

- **Pinned release:** `4.3.2`
- **License:** LGPL-2.0-or-later WITH WxWindows-exception-3.1
- **Parsed scope:** P3 pixels
- **Underlying family:** wxWidgets PNM handler
- **Local input API:** `wx.Image(local path, wx.BITMAP_TYPE_PNM); GetRed/Green/Blue()`
- **Documentation:** [API reference](<https://docs.wxpython.org/wx.Image.html>)
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
