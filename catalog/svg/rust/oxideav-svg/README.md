# oxideav-svg — SVG / Rust

- **Pinned release:** `0.2.0`
- **License:** MIT
- **Parsed scope:** SVG document scene graph and dimensions
- **Underlying family:** oxideav-svg native SVG parser
- **Local input API:** `parse_from(bytes.as_slice()) -> SvgDocument`
- **Documentation:** [API reference](<https://docs.rs/oxideav-svg/0.2.0/oxideav_svg/fn.parse_from.html>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2.0,
  "height": 1.0,
  "nodes": 2
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
