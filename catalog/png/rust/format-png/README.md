# format-png — PNG / Rust

- **Pinned release:** `0.3.0`
- **License:** MIT
- **Parsed scope:** Decoded PNG dimensions and first pixel
- **Underlying family:** format-png engine
- **Local input API:** `decode_rgba8(&[u8])`
- **Documentation:** [API reference](<https://docs.rs/format-png/0.3.0/format_png/>)
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

[Docker harness and verification receipt](../../../../projects/png/rust/format_png/README.md)

```sh
python3 parsarium.py build png rust format_png
python3 parsarium.py run png rust format_png controls/png/red-green.png
```
