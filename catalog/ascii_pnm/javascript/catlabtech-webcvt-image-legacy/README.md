# @catlabtech/webcvt-image-legacy — ASCII PNM / JavaScript

- **Pinned release:** `0.3.0`
- **License:** MIT
- **Parsed scope:** P3 RGB pixels and dimensions
- **Underlying family:** webcvt-image-legacy PPM parser
- **Local input API:** `parsePpm(localUint8Array)`
- **Documentation:** [API reference](<https://unpkg.com/@catlabtech/webcvt-image-legacy@0.3.0/dist/index.d.ts>)
- **Catalog evidence:** [parser record](../../../../data/javascript/ascii_pnm/parsers.json) · [control verification](../../../../data/javascript/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/javascript/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "variant": "ascii",
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
