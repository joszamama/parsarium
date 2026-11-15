# terrio — ASCII PLY / Rust

- **Pinned release:** `0.8.0`
- **License:** MIT AND MPL-2.0 AND Apache-2.0
- **Parsed scope:** ASCII PLY vertex cloud
- **Underlying family:** terrio PLY reader
- **Local input API:** `pointcloud::open_points_bytes(bytes, name).read(&PointReadOptions)`
- **Documentation:** [API reference](<https://docs.rs/terrio/0.8.0/terrio/>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_ply/parsers.json) · [control verification](../../../../data/rust/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
