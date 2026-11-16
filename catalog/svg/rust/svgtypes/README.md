# svgtypes — SVG / Rust

- **Pinned release:** `0.16.2`
- **License:** Apache-2.0 OR MIT
- **Parsed scope:** SVG path command grammar
- **Underlying family:** svgtypes lineage
- **Local input API:** `PathParser::from(path_data).collect()`
- **Documentation:** [API reference](<https://docs.rs/svgtypes/0.16.2/svgtypes/>)
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

[Docker harness and verification receipt](../../../../projects/svg/rust/svgtypes/README.md)

```sh
python3 parsarium.py build svg rust svgtypes
python3 parsarium.py run svg rust svgtypes controls/svg/red-blue-path.svg
```
