# mahotas — ASCII PNM / Python

- **Pinned release:** `1.4.19`
- **License:** MIT
- **Parsed scope:** P3 pixels
- **Underlying family:** mahotas FreeImage
- **Local input API:** `mahotas.imread(local path)`
- **Documentation:** [API reference](<https://mahotas.readthedocs.io/en/latest/api.html>)
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
