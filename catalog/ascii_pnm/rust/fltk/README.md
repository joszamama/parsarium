# fltk — ASCII PNM / Rust

- **Pinned release:** `1.5.23`
- **Upstream:** [source repository](<https://github.com/fltk-rs/fltk-rs>) · [crates.io](<https://crates.io/crates/fltk>)
- **License:** MIT
- **Parsed scope:** P3 ASCII PPM RGB pixels
- **Underlying family:** FLTK C++ PNM image loader
- **Local input API:** `PnmImage::load(control_path)`
- **Documentation:** [API reference](<https://docs.rs/fltk/1.5.23/fltk/image/struct.PnmImage.html#method.load>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_pnm/parsers.json) · [control verification](../../../../data/rust/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "rgb": [
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/rust/fltk/README.md)

```sh
python3 parsarium.py build ascii_pnm rust fltk
python3 parsarium.py run ascii_pnm rust fltk controls/ascii_pnm/red-green.ppm
```
