# zenbitmaps — ASCII PNM / Rust

- **Pinned release:** `0.1.5`
- **Upstream:** [source repository](<https://github.com/imazen/zenbitmaps>) · [crates.io](<https://crates.io/crates/zenbitmaps>)
- **License:** MIT OR Apache-2.0
- **Parsed scope:** P3 ASCII PPM RGB pixels
- **Underlying family:** zenbitmaps PNM decoder
- **Local input API:** `decode(&bytes, enough::Unstoppable)`
- **Documentation:** [API reference](<https://docs.rs/zenbitmaps/0.1.5/zenbitmaps/fn.decode.html>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_pnm/parsers.json) · [control verification](../../../../data/rust/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "layout": "Rgb8",
  "pixels": [
    255,
    0,
    0,
    0,
    255,
    0
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/rust/zenbitmaps/README.md)

```sh
python3 parsarium.py build ascii_pnm rust zenbitmaps
python3 parsarium.py run ascii_pnm rust zenbitmaps controls/ascii_pnm/red-green.ppm
```
