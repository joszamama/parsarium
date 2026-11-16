# spng — PNG / Rust

- **Pinned release:** `0.2.0-alpha.3`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** libspng decoded PNG dimensions and first pixel
- **Underlying family:** libspng native decoder
- **Local input API:** `decode(Cursor, Format::Rgba8)`
- **Documentation:** [API reference](<https://docs.rs/spng/0.2.0-alpha.3/spng/>)
- **Catalog evidence:** [parser record](../../../../data/rust/png/parsers.json) · [control verification](../../../../data/rust/png/verification.json) · [within-ecosystem ranking](../../../../data/rust/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "red_0_0": 255
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/rust/spng/README.md)

```sh
python3 parsarium.py build png rust spng
python3 parsarium.py run png rust spng controls/png/red-green.png
```
