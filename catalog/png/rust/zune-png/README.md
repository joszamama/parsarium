# zune-png — PNG / Rust

- **Pinned release:** `0.5.2`
- **Upstream:** [source repository](<https://github.com/etemesi254/zune-image>) · [crates.io](<https://crates.io/crates/zune-png>)
- **License:** MIT OR Apache-2.0 OR Zlib
- **Parsed scope:** Decoded PNG dimensions and first pixel
- **Underlying family:** zune-png family
- **Local input API:** `PngDecoder::new(Cursor).decode_raw()`
- **Documentation:** [API reference](<https://docs.rs/zune-png/0.5.2/zune_png/>)
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

[Docker harness and verification receipt](../../../../projects/png/rust/zune_png/README.md)

```sh
python3 parsarium.py build png rust zune_png
python3 parsarium.py run png rust zune_png controls/png/red-green.png
```
