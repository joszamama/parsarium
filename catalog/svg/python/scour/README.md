# scour — SVG / Python

- **Pinned release:** `0.38.2`
- **License:** Apache-2.0
- **Parsed scope:** SVG-aware optimization and element tree
- **Underlying family:** Scour SVG XML optimizer
- **Local input API:** `scour.scour.scourString(local_svg_text)`
- **Documentation:** [API reference](<https://github.com/scour-project/scour/blob/v0.38.2/scour/scour.py>)
- **Catalog evidence:** [parser record](../../../../data/python/svg/parsers.json) · [control verification](../../../../data/python/svg/verification.json) · [within-ecosystem ranking](../../../../data/python/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "size": [
    "2",
    "1"
  ],
  "rectangles": 2,
  "optimized_fills": [
    "#f00",
    "#0f0"
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
