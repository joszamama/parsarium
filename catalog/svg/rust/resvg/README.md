# resvg — SVG / Rust

- **Pinned release:** `0.50.0`
- **Upstream:** [source repository](<https://github.com/linebender/resvg>) · [crates.io](<https://crates.io/crates/resvg>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/rust/resvg/README.md)

```sh
python3 parsarium.py build svg rust resvg
python3 parsarium.py run svg rust resvg controls/svg/red-green.svg
```
