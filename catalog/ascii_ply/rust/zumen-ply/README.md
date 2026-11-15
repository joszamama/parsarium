# zumen-ply — ASCII PLY / Rust

- **Pinned release:** `0.2.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** complete ASCII PLY elements and counts
- **Underlying family:** zumen-ply codec
- **Local input API:** `Ply::read(&bytes, &mut Cx)`
- **Documentation:** [API reference](<https://docs.rs/zumen-ply/0.2.0/zumen_ply/>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_ply/parsers.json) · [control verification](../../../../data/rust/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "format": "Ascii"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
