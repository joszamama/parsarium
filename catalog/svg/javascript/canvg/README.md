# canvg — SVG / JavaScript

- **Pinned release:** `4.0.3`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** canvg
- **Local input API:** `Canvg.fromString(canvasContext,svgString,presets.node(...)).render()`
- **Documentation:** [API reference](<https://canvg.js.org/api/classes/Canvg>)
- **Catalog evidence:** [parser record](../../../../data/javascript/svg/parsers.json) · [control verification](../../../../data/javascript/svg/verification.json) · [within-ecosystem ranking](../../../../data/javascript/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgba": [
    255,
    0,
    0,
    255,
    0,
    255,
    0,
    255
  ]
}
```

Uses a supplied DOMParser to construct SVG DOM before rendering.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
