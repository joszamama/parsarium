# unicraft — ASCII PNM / Rust

- **Pinned release:** `0.1.2`
- **License:** GPL-3.0-or-later
- **Parsed scope:** P3 ASCII PPM RGB pixels
- **Underlying family:** unicraft re-export of photocraft PPM reader
- **Local input API:** `photo::Image::read_ppm(&mut BufReader<Cursor<&[u8]>>)`
- **Documentation:** [API reference](<https://docs.rs/unicraft/0.1.2/unicraft/prelude/struct.Image.html#method.read_ppm>)
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
