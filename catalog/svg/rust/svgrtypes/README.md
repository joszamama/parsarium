# svgrtypes — SVG / Rust

- **Pinned release:** `0.50.2`
- **License:** MIT/Apache-2.0
- **Parsed scope:** SVG path command grammar
- **Underlying family:** svgtypes lineage fork
- **Local input API:** `PathParser::from(path_data).collect()`
- **Documentation:** [API reference](<https://docs.rs/svgrtypes/0.50.2/svgrtypes/>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-blue-path.svg`](../../../../controls/svg/red-blue-path.svg)

## Observed control result

```json
{
  "first_command": "M",
  "path_segments": 4
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/rust/svgrtypes/README.md)

```sh
python3 parsarium.py build svg rust svgrtypes
python3 parsarium.py run svg rust svgrtypes controls/svg/red-blue-path.svg
```
