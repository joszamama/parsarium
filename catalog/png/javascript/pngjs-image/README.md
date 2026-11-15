# pngjs-image — PNG / JavaScript

- **Pinned release:** `0.11.7`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** pngjs
- **Local input API:** `PNGImage.loadImage(Buffer, callback)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/pngjs-image>)
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

The pinned package depends on pngjs@2.3.1.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
