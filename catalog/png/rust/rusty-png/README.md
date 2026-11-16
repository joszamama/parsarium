# rusty_png — PNG / Rust

- **Pinned release:** `0.3.2`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** Decoded PNG dimensions and first pixel
- **Underlying family:** image-rs PNG lineage
- **Local input API:** `Decoder::new(Cursor).read_info().next_frame()`
- **Documentation:** [API reference](<https://docs.rs/rusty_png/0.3.2/rusty_png/>)
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

[Docker harness and verification receipt](../../../../projects/png/rust/rusty_png/README.md)

```sh
python3 parsarium.py build png rust rusty_png
python3 parsarium.py run png rust rusty_png controls/png/red-green.png
```
