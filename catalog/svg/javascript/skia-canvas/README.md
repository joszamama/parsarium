# skia-canvas — SVG / JavaScript

- **Pinned release:** `4.0.0`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** Skia
- **Local input API:** `loadImage(Buffer); drawImage()`
- **Documentation:** [API reference](<https://skia-canvas.org/api/image>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/javascript/skia_canvas/README.md)

```sh
python3 parsarium.py build svg javascript skia_canvas
python3 parsarium.py run svg javascript skia_canvas controls/svg/red-green.svg
```
