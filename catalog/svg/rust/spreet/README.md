# spreet — SVG / Rust

- **Pinned release:** `0.14.0`
- **License:** MIT
- **Parsed scope:** SVG document tree and dimensions
- **Underlying family:** usvg lineage via resvg
- **Local input API:** `load_svg(path) -> resvg::usvg::Tree`
- **Documentation:** [API reference](<https://docs.rs/spreet/0.14.0/spreet/>)
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
