# zenbitmaps — ASCII PNM / Rust

- **Pinned release:** `0.1.5`
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
