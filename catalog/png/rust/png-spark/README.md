# png-spark — PNG / Rust

- **Pinned release:** `0.2.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** Decoded PNG dimensions and first pixel
- **Underlying family:** png-spark engine
- **Local input API:** `decode(&[u8])`
- **Documentation:** [API reference](<https://docs.rs/png-spark/0.2.0/png_spark/>)
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

[Docker harness and verification receipt](../../../../projects/png/rust/png_spark/README.md)

```sh
python3 parsarium.py build png rust png_spark
python3 parsarium.py run png rust png_spark controls/png/red-green.png
```
