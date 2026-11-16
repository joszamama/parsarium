# get-svg-colors — SVG / JavaScript

- **Pinned release:** `2.0.1`
- **License:** ISC
- **Parsed scope:** colors
- **Underlying family:** get-svg-colors
- **Local input API:** `getColors(svgString,{flat:true})`
- **Documentation:** [API reference](<https://www.npmjs.com/package/get-svg-colors>)
- **Catalog evidence:** [parser record](../../../../data/javascript/svg/parsers.json) · [control verification](../../../../data/javascript/svg/verification.json) · [within-ecosystem ranking](../../../../data/javascript/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "fills": [
    "#ff0000",
    "#00ff00"
  ]
}
```

Extracts SVG element colors; does not render shapes.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/javascript/get_svg_colors/README.md)

```sh
python3 parsarium.py build svg javascript get_svg_colors
python3 parsarium.py run svg javascript get_svg_colors controls/svg/red-green.svg
```
