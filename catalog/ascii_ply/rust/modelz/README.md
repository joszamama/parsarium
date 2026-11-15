# modelz — ASCII PLY / Rust

- **Pinned release:** `0.1.5`
- **License:** MIT
- **Parsed scope:** ASCII PLY model mesh vertices
- **Underlying family:** ply-rs lineage
- **Local input API:** `Model3D::from_format(path, &ModelFormat::PLY)`
- **Documentation:** [API reference](<https://docs.rs/modelz/0.1.5/modelz/>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_ply/parsers.json) · [control verification](../../../../data/rust/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle-unsigned-face.ply`](../../../../controls/ascii_ply/triangle-unsigned-face.ply)

## Observed control result

```json
{
  "meshes": 1,
  "vertices": 3
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
