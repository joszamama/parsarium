# OpenImageIO — PNG / Python

- **Pinned release:** `3.2.2.0`
- **License:** Apache-2.0
- **Parsed scope:** pixels
- **Underlying family:** OpenImageIO PNG
- **Local input API:** `OpenImageIO.ImageInput.open(local path).read_image()`
- **Documentation:** [API reference](<https://openimageio.readthedocs.io/en/v3.2.1.0/pythonbindings.html>)
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
