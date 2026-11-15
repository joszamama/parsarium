# pycairo — PNG / Python

- **Pinned release:** `1.29.2`
- **License:** LGPL-2.1-only OR MPL-1.1
- **Parsed scope:** pixels
- **Underlying family:** Cairo/libpng
- **Local input API:** `cairo.ImageSurface.create_from_png(local path).get_data()`
- **Documentation:** [API reference](<https://pycairo.readthedocs.io/en/latest/reference/surfaces.html>)
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
