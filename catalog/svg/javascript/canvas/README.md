# canvas — SVG / JavaScript

- **Pinned release:** `3.2.3`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** Cairo/librsvg
- **Local input API:** `loadImage(Buffer); drawImage()`
- **Documentation:** [API reference](<https://github.com/Automattic/node-canvas#loadimage>)
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

Node canvas binding uses the system SVG rendering stack.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/javascript/canvas/README.md)

```sh
python3 parsarium.py build svg javascript canvas
python3 parsarium.py run svg javascript canvas controls/svg/red-green.svg
```
