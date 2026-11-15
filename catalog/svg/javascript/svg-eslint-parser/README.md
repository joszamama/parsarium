# svg-eslint-parser — SVG / JavaScript

- **Pinned release:** `0.5.1`
- **License:** MIT
- **Parsed scope:** structure
- **Underlying family:** svg-eslint-parser
- **Local input API:** `parse(svgString)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/svg-eslint-parser>)
- **Catalog evidence:** [parser record](../../../../data/javascript/svg/parsers.json) · [control verification](../../../../data/javascript/svg/verification.json) · [within-ecosystem ranking](../../../../data/javascript/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rects": 2,
  "fills": [
    "#ff0000",
    "#00ff00"
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
