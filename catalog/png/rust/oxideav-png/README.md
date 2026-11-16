# oxideav-png — PNG / Rust

- **Pinned release:** `0.1.14`
- **License:** MIT
- **Parsed scope:** Decoded PNG dimensions and first pixel
- **Underlying family:** oxideav PNG engine
- **Local input API:** `decode(&[u8])`
- **Documentation:** [API reference](<https://docs.rs/oxideav-png/0.1.14/oxideav_png/>)
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

[Docker harness and verification receipt](../../../../projects/png/rust/oxideav_png/README.md)

```sh
python3 parsarium.py build png rust oxideav_png
python3 parsarium.py run png rust oxideav_png controls/png/red-green.png
```
