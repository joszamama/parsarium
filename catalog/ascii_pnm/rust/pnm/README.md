# pnm — ASCII PNM / Rust

- **Pinned release:** `0.1.1`
- **License:** MIT
- **Parsed scope:** P3 ASCII PPM RGB pixels; pinned release requires nightly feature
- **Underlying family:** pnm crate decoder
- **Local input API:** `decode(&bytes)`
- **Documentation:** [API reference](<https://docs.rs/pnm/0.1.1/pnm/fn.decode.html>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_pnm/parsers.json) · [control verification](../../../../data/rust/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "parsed": "Rgb(Image { buffer: [255, 0, 0, 0, 255, 0], width: 2, height: 1 })"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
