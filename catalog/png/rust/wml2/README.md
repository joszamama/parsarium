# wml2 — PNG / Rust

- **Pinned release:** `0.0.45`
- **License:** MIT
- **Parsed scope:** Decoded PNG dimensions and first pixel
- **Underlying family:** wml2 PNG decoder
- **Local input API:** `draw::image_from_file(path)`
- **Documentation:** [API reference](<https://docs.rs/wml2/0.0.45/wml2/>)
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

[Docker harness and verification receipt](../../../../projects/png/rust/wml2/README.md)

```sh
python3 parsarium.py build png rust wml2
python3 parsarium.py run png rust wml2 controls/png/red-green.png
```
