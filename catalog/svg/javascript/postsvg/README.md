# postsvg — SVG / JavaScript

- **Pinned release:** `2.2.7`
- **License:** MIT
- **Parsed scope:** structure
- **Underlying family:** postsvg/htmlparser2
- **Local input API:** `parse(svgString); tree.select('rect')`
- **Documentation:** [API reference](<https://www.npmjs.com/package/postsvg>)
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

SVG-oriented wrapper over htmlparser2 in XML mode.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
