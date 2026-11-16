# Pillow — ASCII PNM / Python

- **Pinned release:** `13.0.0`
- **License:** MIT-CMU
- **Parsed scope:** P3 pixels
- **Underlying family:** Pillow PPM
- **Local input API:** `PIL.Image.open(local path); load(); getpixel()`
- **Documentation:** [API reference](<https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html#ppm>)
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
