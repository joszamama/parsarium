# draco-io — ASCII PLY / Rust

- **Pinned release:** `0.6.1`
- **Upstream:** [source repository](<https://github.com/Filyus/draco-rust>) · [crates.io](<https://crates.io/crates/draco-io>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/rust/draco_io/README.md)

```sh
python3 parsarium.py build ascii_ply rust draco_io
python3 parsarium.py run ascii_ply rust draco_io controls/ascii_ply/triangle.ply
```
