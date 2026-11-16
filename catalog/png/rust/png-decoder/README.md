# png-decoder — PNG / Rust

- **Pinned release:** `0.2.0`
- **License:** MIT OR Apache-2.0 OR Zlib
- **Parsed scope:** Decoded PNG dimensions and first pixel
- **Underlying family:** png-decoder engine
- **Local input API:** `decode(&[u8])`
- **Documentation:** [API reference](<https://docs.rs/png-decoder/0.2.0/png_decoder/>)
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

[Docker harness and verification receipt](../../../../projects/png/rust/png_decoder/README.md)

```sh
python3 parsarium.py build png rust png_decoder
python3 parsarium.py run png rust png_decoder controls/png/red-green.png
```
