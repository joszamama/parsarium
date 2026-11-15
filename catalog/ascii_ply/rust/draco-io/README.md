# draco-io — ASCII PLY / Rust

- **Pinned release:** `0.6.1`
- **License:** Apache-2.0
- **Parsed scope:** ASCII PLY vertex positions
- **Underlying family:** draco-io PLY reader
- **Local input API:** `ply_reader::PlyReader::from_bytes(bytes).read_positions()`
- **Documentation:** [API reference](<https://docs.rs/draco-io/0.6.1/draco_io/>)
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
