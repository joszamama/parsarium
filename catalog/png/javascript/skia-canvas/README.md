# skia-canvas — PNG / JavaScript

- **Pinned release:** `4.0.0`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** Skia
- **Local input API:** `loadImage(Buffer); drawImage; getImageData`
- **Documentation:** [API reference](<https://skia-canvas.org/api/image>)
- **Catalog evidence:** [parser record](../../../../data/javascript/png/parsers.json) · [control verification](../../../../data/javascript/png/verification.json) · [within-ecosystem ranking](../../../../data/javascript/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

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

[Docker harness and verification receipt](../../../../projects/png/javascript/skia_canvas/README.md)

```sh
python3 parsarium.py build png javascript skia_canvas
python3 parsarium.py run png javascript skia_canvas controls/png/red-green.png
```
