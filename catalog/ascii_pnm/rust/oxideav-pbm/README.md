# oxideav-pbm — ASCII PNM / Rust

- **Pinned release:** `0.0.5`
- **License:** MIT
- **Parsed scope:** P3 ASCII PPM RGB pixels
- **Underlying family:** OxideAV PBM decoder
- **Local input API:** `decode_pbm(&bytes)`
- **Documentation:** [API reference](<https://docs.rs/oxideav-pbm/0.0.5/oxideav_pbm/decoder/fn.decode_pbm.html>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_pnm/parsers.json) · [control verification](../../../../data/rust/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "format": "Rgb24",
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/rust/oxideav_pbm/README.md)

```sh
python3 parsarium.py build ascii_pnm rust oxideav_pbm
python3 parsarium.py run ascii_pnm rust oxideav_pbm controls/ascii_pnm/red-green.ppm
```
