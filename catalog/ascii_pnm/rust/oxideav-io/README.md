# oxideav-io — ASCII PNM / Rust

- **Pinned release:** `0.1.2`
- **License:** MIT
- **Parsed scope:** P3 ASCII PPM RGB pixels
- **Underlying family:** OxideAV I/O gateway over oxideav-image and oxideav-pbm
- **Local input API:** `open_image_with(&RuntimeContext with oxideav-pbm registered, Source::bytes(&bytes), &OpenOptions::eager())`
- **Documentation:** [API reference](<https://docs.rs/oxideav-io/0.1.2/oxideav_io/fn.open_image_with.html>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
