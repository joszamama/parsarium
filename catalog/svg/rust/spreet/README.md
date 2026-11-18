# spreet — SVG / Rust

- **Pinned release:** `0.14.0`
- **Upstream:** [source repository](<https://github.com/flother/spreet>) · [crates.io](<https://crates.io/crates/spreet>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/rust/spreet/README.md)

```sh
python3 parsarium.py build svg rust spreet
python3 parsarium.py run svg rust spreet controls/svg/red-green.svg
```
