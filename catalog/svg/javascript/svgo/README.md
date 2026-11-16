# svgo — SVG / JavaScript

- **Pinned release:** `4.1.0`
- **License:** MIT
- **Parsed scope:** optimized_paths
- **Underlying family:** SVGO
- **Local input API:** `optimize(svgString,{plugins:['convertShapeToPath']})`
- **Documentation:** [API reference](<https://svgo.dev/docs/introduction/>)
- **Catalog evidence:** [parser record](../../../../data/javascript/svg/parsers.json) · [control verification](../../../../data/javascript/svg/verification.json) · [within-ecosystem ranking](../../../../data/javascript/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "paths": 2,
  "fills": [
    "#ff0000",
    "#00ff00"
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/javascript/svgo/README.md)

```sh
python3 parsarium.py build svg javascript svgo
python3 parsarium.py run svg javascript svgo controls/svg/red-green.svg
```
