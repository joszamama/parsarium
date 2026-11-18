# usvg-parser — SVG / Rust

- **Pinned release:** `0.38.0`
- **Upstream:** [source repository](<https://github.com/linebender/resvg>) · [crates.io](<https://crates.io/crates/usvg-parser>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/rust/usvg_parser/README.md)

```sh
python3 parsarium.py build svg rust usvg_parser
python3 parsarium.py run svg rust usvg_parser controls/svg/red-green.svg
```
