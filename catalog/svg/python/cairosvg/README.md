# CairoSVG — SVG / Python

- **Pinned release:** `2.9.1`
- **License:** LGPL-3.0-or-later
- **Parsed scope:** SVG rendering with dimensions and colored pixels
- **Underlying family:** CairoSVG Python SVG parser plus Cairo renderer
- **Local input API:** `cairosvg.svg2png(bytestring=local_svg_bytes)`
- **Documentation:** [API reference](<https://cairosvg.org/documentation/index.html>)
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
