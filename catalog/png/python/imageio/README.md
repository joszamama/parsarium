# imageio — PNG / Python

- **Pinned release:** `2.38.1`
- **License:** BSD-2-Clause
- **Parsed scope:** pixels
- **Underlying family:** ImageIO via Pillow
- **Local input API:** `imageio.v3.imread(local path)`
- **Documentation:** [API reference](<https://imageio.readthedocs.io/en/stable/reference/userapi.html>)
- **Catalog evidence:** [parser record](../../../../data/python/png/parsers.json) · [control verification](../../../../data/python/png/verification.json) · [within-ecosystem ranking](../../../../data/python/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgba0": [
    255,
    0,
    0,
    255
  ],
  "rgba1": [
    0,
    255,
    0,
    255
  ]
}
```

Observed or documented wrapper path; this package is counted as a distinct API package, not an independent PNG engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
