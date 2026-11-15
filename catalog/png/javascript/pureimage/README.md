# pureimage — PNG / JavaScript

- **Pinned release:** `0.4.20`
- **License:** MIT
- **Parsed scope:** pixels
- **Underlying family:** pngjs
- **Local input API:** `decodePNGFromStream(Readable)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/pureimage>)
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

The pinned package depends on pngjs@^7.0.0.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
