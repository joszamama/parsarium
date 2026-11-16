# tiny-image-size — ASCII PNM / JavaScript

- **Pinned release:** `1.0.0`
- **License:** MIT
- **Parsed scope:** P3 header dimensions and PNM type
- **Underlying family:** tiny-image-size PNM header reader
- **Local input API:** `tinyImageSize(localUint8Array)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/tiny-image-size>)
- **Catalog evidence:** [parser record](../../../../data/javascript/ascii_pnm/parsers.json) · [control verification](../../../../data/javascript/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/javascript/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "type": "pnm",
  "width": 2,
  "height": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
