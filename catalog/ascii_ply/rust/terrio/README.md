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

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/rust/terrio/README.md)

```sh
python3 parsarium.py build ascii_ply rust terrio
python3 parsarium.py run ascii_ply rust terrio controls/ascii_ply/triangle.ply
```
