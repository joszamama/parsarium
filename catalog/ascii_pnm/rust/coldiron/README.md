# coldiron — ASCII PNM / Rust

- **Pinned release:** `0.1.0`
- **License:** MIT
- **Parsed scope:** P2 ASCII PGM grayscale pixels
- **Underlying family:** coldiron Netpbm reader
- **Local input API:** `Image::read_from(&mut Cursor::new(&bytes))`
- **Documentation:** [API reference](<https://docs.rs/coldiron/0.1.0/coldiron/struct.Image.html#method.read_from>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_pnm/parsers.json) · [control verification](../../../../data/rust/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/black-white.pgm`](../../../../controls/ascii_pnm/black-white.pgm)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "format": "Graymap",
  "pixels": [
    0,
    255
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
