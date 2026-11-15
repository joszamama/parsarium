# netpbm — ASCII PNM / Python

- **Pinned release:** `0.0.1`
- **License:** GPL-3.0-or-later
- **Parsed scope:** P3 pixels
- **Underlying family:** netpbm pure Python
- **Local input API:** `netpbm.ImgColor(width,height).from_file(local path)`
- **Documentation:** [API reference](<https://github.com/juancarlospaco/netpbm#reference>)
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
