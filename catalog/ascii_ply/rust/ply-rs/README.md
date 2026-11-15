# ply-rs — ASCII PLY / Rust

- **Pinned release:** `0.1.3`
- **License:** MIT
- **Parsed scope:** complete ASCII PLY: header, vertices, faces
- **Underlying family:** ply-rs lineage
- **Local input API:** `Parser::<DefaultElement>::read_ply(&mut Cursor<&[u8]>)`
- **Documentation:** [API reference](<https://docs.rs/ply-rs/0.1.3/ply_rs/>)
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
