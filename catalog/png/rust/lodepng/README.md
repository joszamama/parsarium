# lodepng — PNG / Rust

- **Pinned release:** `3.12.2`
- **License:** Zlib
- **Parsed scope:** Decoded PNG dimensions and first pixel
- **Underlying family:** LodePNG family
- **Local input API:** `decode32_file(path)`
- **Documentation:** [API reference](<https://docs.rs/lodepng/3.12.2/lodepng/>)
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

[Docker harness and verification receipt](../../../../projects/png/rust/lodepng/README.md)

```sh
python3 parsarium.py build png rust lodepng
python3 parsarium.py run png rust lodepng controls/png/red-green.png
```
