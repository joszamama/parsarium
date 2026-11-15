# resvg — SVG / Rust

- **Pinned release:** `0.50.0`
- **License:** Apache-2.0 OR MIT
- **Parsed scope:** SVG raster rendering
- **Underlying family:** usvg lineage
- **Local input API:** `usvg::Tree::from_data(&bytes, &Options::default()); render(&tree, transform, pixmap)`
- **Documentation:** [API reference](<https://docs.rs/resvg/0.50.0/resvg/>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2.0,
  "height": 1.0,
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
