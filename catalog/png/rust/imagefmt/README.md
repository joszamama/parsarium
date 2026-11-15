# imagefmt — PNG / Rust

- **Pinned release:** `4.0.0`
- **License:** MIT
- **Parsed scope:** Decoded PNG dimensions and first pixel
- **Underlying family:** imagefmt PNG engine
- **Local input API:** `read_from(&mut Cursor, ColFmt::RGBA)`
- **Documentation:** [API reference](<https://docs.rs/imagefmt/4.0.0/imagefmt/>)
- **Catalog evidence:** [parser record](../../../../data/rust/png/parsers.json) · [control verification](../../../../data/rust/png/verification.json) · [within-ecosystem ranking](../../../../data/rust/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1,
  "red_0_0": 255
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
