# ply2splat — ASCII PLY / Rust

- **Pinned release:** `0.6.0`
- **License:** MIT
- **Parsed scope:** ASCII PLY vertex positions into Gaussian-splat records
- **Underlying family:** ply-rs lineage
- **Local input API:** `load_ply_from_bytes(&bytes)`
- **Documentation:** [API reference](<https://docs.rs/ply2splat/0.6.0/ply2splat/>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_ply/parsers.json) · [control verification](../../../../data/rust/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "last_vertex": [
    0.0,
    1.0,
    0.0
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
