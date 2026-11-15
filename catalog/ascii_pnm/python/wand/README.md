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

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/python/wand/README.md)

```sh
python3 parsarium.py build ascii_pnm python wand
python3 parsarium.py run ascii_pnm python wand controls/ascii_pnm/red-green.ppm
```
