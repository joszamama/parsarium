# usvg-parser — SVG / Rust

- **Pinned release:** `0.38.0`
- **License:** MPL-2.0
- **Parsed scope:** SVG document tree and dimensions
- **Underlying family:** usvg lineage
- **Local input API:** `TreeParsing::from_data(&bytes, &Options::default()) on usvg_tree::Tree`
- **Documentation:** [API reference](<https://docs.rs/usvg-parser/0.38.0/usvg_parser/>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "width": 2.0,
  "height": 1.0
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
