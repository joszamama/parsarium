# threecrate-io — ASCII PLY / Rust

- **Pinned release:** `0.12.1`
- **Upstream:** [source repository](<https://github.com/rajgandhi1/threecrate>) · [crates.io](<https://crates.io/crates/threecrate-io>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/rust/threecrate_io/README.md)

```sh
python3 parsarium.py build ascii_ply rust threecrate_io
python3 parsarium.py run ascii_ply rust threecrate_io controls/ascii_ply/triangle.ply
```
