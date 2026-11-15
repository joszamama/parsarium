# Pillow — PNG / Python

- **Pinned release:** `13.0.0`
- **License:** MIT-CMU
- **Parsed scope:** pixels
- **Underlying family:** Pillow PNG
- **Local input API:** `Image.open(local path); Image.load(); Image.getpixel`
- **Documentation:** [API reference](<https://pillow.readthedocs.io/en/stable/reference/open_files.html>)
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
