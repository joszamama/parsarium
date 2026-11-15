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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
