# wblidar — ASCII PLY / Rust

- **Pinned release:** `0.1.3`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** ASCII PLY point records
- **Underlying family:** wblidar PLY reader
- **Local input API:** `ply::PlyReader::new(Cursor<&[u8]>).read_all()`
- **Documentation:** [API reference](<https://docs.rs/wblidar/0.1.3/wblidar/>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/rust/wblidar/README.md)

```sh
python3 parsarium.py build ascii_ply rust wblidar
python3 parsarium.py run ascii_ply rust wblidar controls/ascii_ply/triangle.ply
```
