# threecrate — ASCII PLY / Rust

- **Pinned release:** `0.12.1`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** ASCII PLY vertices and faces via threecrate facade
- **Underlying family:** threecrate RobustPlyReader
- **Local input API:** `io::ply::RobustPlyReader::read_ply_data(&mut BufReader<Cursor<&[u8]>>)`
- **Documentation:** [API reference](<https://docs.rs/threecrate/0.12.1/threecrate/>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_ply/parsers.json) · [control verification](../../../../data/rust/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/rust/threecrate/README.md)

```sh
python3 parsarium.py build ascii_ply rust threecrate
python3 parsarium.py run ascii_ply rust threecrate controls/ascii_ply/triangle.ply
```
