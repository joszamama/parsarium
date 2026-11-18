# svg_path_ops — SVG / Rust

- **Pinned release:** `0.12.0`
- **Upstream:** [source repository](<https://github.com/orhanbalci/rough-rs>) · [crates.io](<https://crates.io/crates/svg_path_ops>)
- **License:** MIT
- **Parsed scope:** SVG path command grammar and serialization
- **Underlying family:** svgtypes lineage via svg_path_ops
- **Local input API:** `pt::PathTransformer::parse(path_data).to_string()`
- **Documentation:** [API reference](<https://docs.rs/svg_path_ops/0.12.0/svg_path_ops/pt/struct.PathTransformer.html>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-blue-path.svg`](../../../../controls/svg/red-blue-path.svg)

## Observed control result

```json
{
  "serialized": "M 2 0 L 4 0 L 4 2 Z"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/rust/svg_path_ops/README.md)

```sh
python3 parsarium.py build svg rust svg_path_ops
python3 parsarium.py run svg rust svg_path_ops controls/svg/red-blue-path.svg
```
