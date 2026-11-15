# ps-usvg — SVG / Rust

- **Pinned release:** `0.48.1`
- **License:** Apache-2.0 OR MIT
- **Parsed scope:** SVG document tree and dimensions
- **Underlying family:** ps-usvg fork of usvg lineage
- **Local input API:** `Tree::from_data(&bytes, &Options::default())`
- **Documentation:** [API reference](<https://docs.rs/ps-usvg/0.48.1/usvg/>)
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
