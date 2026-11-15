# @napi-rs/canvas — PNG / JavaScript

- **Pinned release:** `1.1.0`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** Skia
- **Local input API:** `loadImage(Buffer); drawImage; getImageData`
- **Documentation:** [API reference](<https://github.com/Brooooooklyn/canvas/blob/main/index.d.ts>)
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

Native Node-API binding; pinned package type declarations document Buffer input.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
