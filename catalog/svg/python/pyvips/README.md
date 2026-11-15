# pyvips — SVG / Python

- **Pinned release:** `3.2.0`
- **License:** MIT
- **Parsed scope:** SVG rendering with dimensions and colored pixels
- **Underlying family:** libvips SVG loader (librsvg)
- **Local input API:** `pyvips.Image.new_from_file(local_svg_path)`
- **Documentation:** [API reference](<https://libvips.github.io/pyvips/vimage.html>)
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
