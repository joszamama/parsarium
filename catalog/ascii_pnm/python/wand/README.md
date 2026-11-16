# Wand — ASCII PNM / Python

- **Pinned release:** `0.7.2`
- **License:** MIT
- **Parsed scope:** P3 pixels
- **Underlying family:** ImageMagick PNM
- **Local input API:** `wand.image.Image(filename=local path); export_pixels()`
- **Documentation:** [API reference](<https://docs.wand-py.org/en/latest/guide/read.html>)
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
