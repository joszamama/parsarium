# rs-read-trimesh — ASCII PLY / Rust

- **Pinned release:** `2.1.1`
- **License:** MIT
- **Parsed scope:** ASCII PLY triangle mesh vertices and faces
- **Underlying family:** ply-rs-bw fork
- **Local input API:** `load_trimesh(path, scale)`
- **Documentation:** [API reference](<https://docs.rs/rs-read-trimesh/2.1.1/rs_read_trimesh/>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_ply/parsers.json) · [control verification](../../../../data/rust/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
