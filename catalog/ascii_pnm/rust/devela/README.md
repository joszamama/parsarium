# devela — ASCII PNM / Rust

- **Pinned release:** `0.30.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** P3 ASCII PPM RGB pixels
- **Underlying family:** devela PNM decoder
- **Local input API:** `Pnm::decoded_len_u8(&bytes); Pnm::decode_u8(&bytes, &mut pixels)`
- **Documentation:** [API reference](<https://docs.rs/devela/0.30.0/devela/media/visual/image/format/struct.Pnm.html>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_pnm/parsers.json) · [control verification](../../../../data/rust/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "size": "Extent { dim: [2, 1] }",
  "channels": 3,
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/rust/devela/README.md)

```sh
python3 parsarium.py build ascii_pnm rust devela
python3 parsarium.py run ascii_pnm rust devela controls/ascii_pnm/red-green.ppm
```
