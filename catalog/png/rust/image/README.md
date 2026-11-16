# image — PNG / Rust

- **Pinned release:** `0.25.10`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** Decoded PNG dimensions and first pixel
- **Underlying family:** image-rs PNG lineage
- **Local input API:** `load_from_memory(&[u8])`
- **Documentation:** [API reference](<https://docs.rs/image/0.25.10/image/>)
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

[Docker harness and verification receipt](../../../../projects/png/rust/image/README.md)

```sh
python3 parsarium.py build png rust image
python3 parsarium.py run png rust image controls/png/red-green.png
```
