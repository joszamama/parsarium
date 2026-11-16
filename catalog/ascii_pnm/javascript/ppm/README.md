# ppm — ASCII PNM / JavaScript

- **Pinned release:** `0.0.0`
- **License:** BSD
- **Parsed scope:** P3 RGB pixels and dimensions
- **Underlying family:** ppm streaming parser
- **Local input API:** `parse(createReadStream(localPath), callback)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/ppm>)
- **Catalog evidence:** [parser record](../../../../data/javascript/ascii_pnm/parsers.json) · [control verification](../../../../data/javascript/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/javascript/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgb": [
    255,
    0,
    0,
    0,
    255,
    0
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
