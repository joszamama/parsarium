# netpbm-parser — ASCII PNM / JavaScript

- **Pinned release:** `1.1.7`
- **License:** MIT
- **Parsed scope:** P3 RGB pixels and dimensions
- **Underlying family:** netpbm-parser
- **Local input API:** `parse(localAsciiString, 1)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/netpbm-parser>)
- **Catalog evidence:** [parser record](../../../../data/javascript/ascii_pnm/parsers.json) · [control verification](../../../../data/javascript/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/javascript/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "type": "P3",
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
