# cortenforge-mesh-io — ASCII PLY / Rust

- **Pinned release:** `0.9.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** ASCII PLY mesh vertices and faces
- **Underlying family:** ply-rs lineage
- **Local input API:** `mesh_io::load_ply(path)`
- **Documentation:** [API reference](<https://docs.rs/cortenforge-mesh-io/0.9.0/mesh_io/>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/rust/cortenforge_mesh_io/README.md)

```sh
python3 parsarium.py build ascii_ply rust cortenforge_mesh_io
python3 parsarium.py run ascii_ply rust cortenforge_mesh_io controls/ascii_ply/triangle.ply
```
