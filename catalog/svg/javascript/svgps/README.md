# svgps — SVG / JavaScript

- **Pinned release:** `0.9.0`
- **License:** MIT
- **Parsed scope:** paths
- **Underlying family:** svgps
- **Local input API:** `parse(svgString)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/svgps>)
- **Catalog evidence:** [parser record](../../../../data/javascript/svg/parsers.json) · [control verification](../../../../data/javascript/svg/verification.json) · [within-ecosystem ranking](../../../../data/javascript/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "paths": 2,
  "fills": [
    "#ff0000",
    "#00ff00"
  ]
}
```

Converts SVG rectangle elements into path records.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
