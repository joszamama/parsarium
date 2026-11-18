# minipng — PNG / Rust

- **Pinned release:** `1.0.0`
- **Upstream:** [source repository](<https://github.com/pommicket/minipng>) · [crates.io](<https://crates.io/crates/minipng>)
- **License:** 0BSD
- **Parsed scope:** Decoded PNG dimensions and first pixel
- **Underlying family:** minipng decoder
- **Local input API:** `decode_png_header(&[u8]); decode_png(&[u8], &mut [u8])`
- **Documentation:** [API reference](<https://docs.rs/minipng/1.0.0/minipng/>)
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

[Docker harness and verification receipt](../../../../projects/png/rust/minipng/README.md)

```sh
python3 parsarium.py build png rust minipng
python3 parsarium.py run png rust minipng controls/png/red-green.png
```
