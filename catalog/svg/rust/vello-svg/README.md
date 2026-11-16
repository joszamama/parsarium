# vello_svg — SVG / Rust

- **Pinned release:** `0.11.0`
- **License:** Apache-2.0 OR MIT
- **Parsed scope:** SVG render path encoding
- **Underlying family:** usvg lineage via vello_svg
- **Local input API:** `render(svg_text) -> vello::Scene`
- **Documentation:** [API reference](<https://docs.rs/vello_svg/0.11.0/vello_svg/>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "paths": 2,
  "path_segments": 8
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/rust/vello_svg/README.md)

```sh
python3 parsarium.py build svg rust vello_svg
python3 parsarium.py run svg rust vello_svg controls/svg/red-green.svg
```
