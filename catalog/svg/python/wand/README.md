# Wand — SVG / Python

- **Pinned release:** `0.7.2`
- **License:** MIT
- **Parsed scope:** SVG rendering with dimensions and colored pixels
- **Underlying family:** ImageMagick SVG coder through Wand
- **Local input API:** `wand.image.Image(filename=local_svg_path)`
- **Documentation:** [API reference](<https://docs.wand-py.org/en/latest/guide/read.html>)
- **Catalog evidence:** [parser record](../../../../data/python/svg/parsers.json) · [control verification](../../../../data/python/svg/verification.json) · [within-ecosystem ranking](../../../../data/python/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "size": [
    2,
    1
  ],
  "red": [
    255,
    0,
    0,
    255
  ],
  "green": [
    0,
    255,
    0,
    255
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
