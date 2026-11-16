# oxvg_path — SVG / Rust

- **Pinned release:** `0.0.9`
- **License:** MIT
- **Parsed scope:** SVG path command grammar
- **Underlying family:** oxvg_path + oxvg_parse
- **Local input API:** `Path::parse_string(path_data)`
- **Documentation:** [API reference](<https://docs.rs/oxvg_path/0.0.9/oxvg_path/>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-blue-path.svg`](../../../../controls/svg/red-blue-path.svg)

## Observed control result

```json
{
  "path_commands": 4,
  "serialized": "M2 0 4 0 4 2Z"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/rust/oxvg_path/README.md)

```sh
python3 parsarium.py build svg rust oxvg_path
python3 parsarium.py run svg rust oxvg_path controls/svg/red-blue-path.svg
```
