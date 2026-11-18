# serde-ply — ASCII PLY / Rust

- **Pinned release:** `0.2.2`
- **Upstream:** [source repository](<https://github.com/ArthurBrussee/serde_ply>) · [crates.io](<https://crates.io/crates/serde-ply>)
- **License:** Apache-2.0
- **Parsed scope:** typed ASCII PLY vertices and face indices
- **Underlying family:** serde-ply
- **Local input API:** `from_bytes::<Mesh>(&bytes)`
- **Documentation:** [API reference](<https://docs.rs/serde-ply/0.2.2/serde_ply/>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_ply/parsers.json) · [control verification](../../../../data/rust/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "last_vertex": [
    0.0,
    1.0,
    0.0
  ],
  "first_face": [
    0,
    1,
    2
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/rust/serde_ply/README.md)

```sh
python3 parsarium.py build ascii_ply rust serde_ply
python3 parsarium.py run ascii_ply rust serde_ply controls/ascii_ply/triangle.ply
```
