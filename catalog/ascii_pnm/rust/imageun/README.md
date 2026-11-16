# imageun — ASCII PNM / Rust

- **Pinned release:** `0.0.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** P3 ASCII PPM RGB pixels
- **Underlying family:** image-rs fork
- **Local input API:** `load_from_memory_with_format(&bytes, ImageFormat::Pnm)`
- **Documentation:** [API reference](<https://docs.rs/imageun/0.0.0/imageun/fn.load_from_memory_with_format.html>)
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/rust/imageun/README.md)

```sh
python3 parsarium.py build ascii_pnm rust imageun
python3 parsarium.py run ascii_pnm rust imageun controls/ascii_pnm/red-green.ppm
```
