# makepad-zune-png — PNG / Rust

- **Pinned release:** `0.4.10`
- **License:** MIT OR Apache-2.0 OR Zlib
- **Parsed scope:** Decoded PNG first pixel and byte count
- **Underlying family:** zune-png family
- **Local input API:** `PngDecoder::new(&[u8]).decode_raw()`
- **Documentation:** [API reference](<https://docs.rs/makepad-zune-png/0.4.10/makepad_zune_png/>)
- **Catalog evidence:** [parser record](../../../../data/rust/png/parsers.json) · [control verification](../../../../data/rust/png/verification.json) · [within-ecosystem ranking](../../../../data/rust/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "red_0_0": 255,
  "pixel_bytes": 8
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/png/rust/makepad_zune_png/README.md)

```sh
python3 parsarium.py build png rust makepad_zune_png
python3 parsarium.py run png rust makepad_zune_png controls/png/red-green.png
```
