# @yworks/canvg — SVG / JavaScript

- **Pinned release:** `4.0.4`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** canvg
- **Local input API:** `Canvg.fromString(canvasContext,svgString,presets.node(...)).render()`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@yworks/canvg>)
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

Fork/distribution of canvg.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/javascript/yworks_canvg/README.md)

```sh
python3 parsarium.py build svg javascript yworks_canvg
python3 parsarium.py run svg javascript yworks_canvg controls/svg/red-green.svg
```
