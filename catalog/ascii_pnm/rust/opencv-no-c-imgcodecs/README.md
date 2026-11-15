# opencv-no-c-imgcodecs — ASCII PNM / Rust

- **Pinned release:** `0.1.0`
- **License:** Apache-2.0
- **Parsed scope:** P3 ASCII PPM BGR pixels
- **Underlying family:** opencv-no-c PNM decoder
- **Local input API:** `pnm::decode(&bytes)`
- **Documentation:** [API reference](<https://docs.rs/opencv-no-c-imgcodecs/0.1.0/cv_imgcodecs/pnm/fn.decode.html>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_pnm/parsers.json) · [control verification](../../../../data/rust/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "bgr": [
    0,
    0,
    255,
    0,
    255,
    0
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
