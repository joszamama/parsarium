# @napi-rs/image — ASCII PNM / JavaScript

- **Pinned release:** `1.16.0`
- **License:** MIT
- **Parsed scope:** P3 header dimensions and PNM type
- **Underlying family:** napi-rs/image Rust image crate PNM decoder
- **Local input API:** `new Transformer(localBuffer).metadata()`
- **Documentation:** [API reference](<https://github.com/Brooooooklyn/Image/blob/main/README.md>)
- **Catalog evidence:** [parser record](../../../../data/javascript/ascii_pnm/parsers.json) · [control verification](../../../../data/javascript/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/javascript/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "format": "pnm",
  "width": 2,
  "height": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
