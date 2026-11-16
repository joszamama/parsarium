# brepkit-io — ASCII PLY / Rust

- **Pinned release:** `4.11.3`
- **License:** AGPL-3.0-only
- **Parsed scope:** ASCII PLY triangle mesh vertices and faces
- **Underlying family:** brepkit PLY reader
- **Local input API:** `ply::read_ply(&bytes)`
- **Documentation:** [API reference](<https://docs.rs/brepkit-io/4.11.3/brepkit_io/>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/rust/brepkit_io/README.md)

```sh
python3 parsarium.py build ascii_ply rust brepkit_io
python3 parsarium.py run ascii_ply rust brepkit_io controls/ascii_ply/triangle.ply
```
