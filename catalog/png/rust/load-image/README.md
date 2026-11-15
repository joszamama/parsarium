# load_image — PNG / Rust

- **Pinned release:** `3.5.0`
- **License:** BSD-3-Clause
- **Parsed scope:** Decoded PNG dimensions via LodePNG
- **Underlying family:** LodePNG family
- **Local input API:** `load_data(&[u8])`
- **Documentation:** [API reference](<https://docs.rs/load_image/3.5.0/load_image/>)
- **Catalog evidence:** [parser record](../../../../data/rust/png/parsers.json) · [control verification](../../../../data/rust/png/verification.json) · [within-ecosystem ranking](../../../../data/rust/png/ranking.md)
- **Valid control:** [`controls/png/red-green.png`](../../../../controls/png/red-green.png)

## Observed control result

```json
{
  "width": 2,
  "height": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
