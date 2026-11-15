# threecrate-io — ASCII PLY / Rust

- **Pinned release:** `0.12.1`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** complete ASCII PLY: header, vertices, faces
- **Underlying family:** threecrate RobustPlyReader
- **Local input API:** `ply::RobustPlyReader::read_ply_data(&mut BufReader<Cursor<&[u8]>>)`
- **Documentation:** [API reference](<https://docs.rs/threecrate-io/0.12.1/threecrate_io/>)
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
