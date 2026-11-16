# image-size — ASCII PNM / JavaScript

- **Pinned release:** `2.1.0`
- **License:** MIT
- **Parsed scope:** P3 header dimensions and PNM type
- **Underlying family:** image-size PNM header reader
- **Local input API:** `imageSize(localBuffer)`
- **Documentation:** [API reference](<https://github.com/image-size/image-size#usage>)
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
