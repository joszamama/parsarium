# pgmjs — ASCII PNM / JavaScript

- **Pinned release:** `1.1.6`
- **License:** ISC
- **Parsed scope:** P2 grayscale pixels and dimensions
- **Underlying family:** pgmjs
- **Local input API:** `readPgm(localFilePath)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/pgmjs>)
- **Catalog evidence:** [parser record](../../../../data/javascript/ascii_pnm/parsers.json) · [control verification](../../../../data/javascript/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/javascript/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/black-white.pgm`](../../../../controls/ascii_pnm/black-white.pgm)

## Observed control result

```json
{
  "type": "P2",
  "width": 2,
  "height": 1,
  "maxval": 255,
  "pixels": [
    0,
    255
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
