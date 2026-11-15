# rasterio — PNG / Python

- **Pinned release:** `1.5.2`
- **License:** BSD-3-Clause
- **Parsed scope:** pixels
- **Underlying family:** GDAL PNG
- **Local input API:** `rasterio.open(local path).read()`
- **Documentation:** [API reference](<https://rasterio.readthedocs.io/en/stable/quickstart.html>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
