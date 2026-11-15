# svg_metadata — SVG / Rust

- **Pinned release:** `0.6.0`
- **License:** Apache-2.0/MIT
- **Parsed scope:** SVG viewBox metadata
- **Underlying family:** svg_metadata + roxmltree
- **Local input API:** `Metadata::parse_file(path).view_box`
- **Documentation:** [API reference](<https://docs.rs/svg_metadata/0.6.0/svg_metadata/>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "viewbox_width": 2.0,
  "viewbox_height": 1.0
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
