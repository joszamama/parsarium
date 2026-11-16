# svglab — SVG / Python

- **Pinned release:** `0.18.0`
- **License:** MIT
- **Parsed scope:** SVG typed element tree and colors
- **Underlying family:** svglab Rust/Python typed SVG tree
- **Local input API:** `svglab.parse_svg(local_svg_bytes)`
- **Documentation:** [API reference](<https://pypi.org/project/svglab/0.18.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/svg/parsers.json) · [control verification](../../../../data/python/svg/verification.json) · [within-ecosystem ranking](../../../../data/python/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "size": [
    2,
    1
  ],
  "fills": [
    "red",
    "lime"
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
