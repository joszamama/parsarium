# voxel-tiler-core — ASCII PLY / Rust

- **Pinned release:** `0.3.2`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** ASCII PLY vertex cloud
- **Underlying family:** ply-rs lineage
- **Local input API:** `PointCloud::<OrderedFloat<f32>,u8,u8>::from_ply(Cursor<&[u8]>)`
- **Documentation:** [API reference](<https://docs.rs/voxel-tiler-core/0.3.2/voxel_tiler_core/>)
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
