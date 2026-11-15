# imageio — ASCII PNM / Python

- **Pinned release:** `2.38.1`
- **License:** BSD-2-Clause
- **Parsed scope:** P3 pixels
- **Underlying family:** ImageIO via Pillow PPM
- **Local input API:** `imageio.v3.imread(local path)`
- **Documentation:** [API reference](<https://imageio.readthedocs.io/en/stable/reference/userapi.html>)
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
