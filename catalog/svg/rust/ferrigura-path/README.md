# ferrigura-path — SVG / Rust

- **Pinned release:** `0.7.0`
- **License:** MIT AND BSD-3-Clause
- **Parsed scope:** SVG path geometry
- **Underlying family:** Blink/Skia SVG path port
- **Local input API:** `bounding_box(path_data)`
- **Documentation:** [API reference](<https://docs.rs/ferrigura-path/0.7.0/ferrigura_path/>)
- **Catalog evidence:** [parser record](../../../../data/rust/svg/parsers.json) · [control verification](../../../../data/rust/svg/verification.json) · [within-ecosystem ranking](../../../../data/rust/svg/ranking.md)
- **Valid control:** [`controls/svg/red-blue-path.svg`](../../../../controls/svg/red-blue-path.svg)

## Observed control result

```json
{
  "x": 2.0,
  "y": 0.0,
  "width": 2.0,
  "height": 2.0
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/rust/ferrigura_path/README.md)

```sh
python3 parsarium.py build svg rust ferrigura_path
python3 parsarium.py run svg rust ferrigura_path controls/svg/red-blue-path.svg
```
