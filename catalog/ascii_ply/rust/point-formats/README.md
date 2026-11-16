# point-formats — ASCII PLY / Rust

- **Pinned release:** `0.3.1`
- **License:** MIT
- **Parsed scope:** ASCII PLY mesh vertices and faces
- **Underlying family:** point-formats native PLY codec
- **Local input API:** `io::ply::read(&mut BufReader<Cursor<&[u8]>>)`
- **Documentation:** [API reference](<https://docs.rs/point-formats/0.3.1/point_formats/>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/rust/point_formats/README.md)

```sh
python3 parsarium.py build ascii_ply rust point_formats
python3 parsarium.py run ascii_ply rust point_formats controls/ascii_ply/triangle.ply
```
