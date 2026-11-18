# rs-read-trimesh — ASCII PLY / Rust

- **Pinned release:** `2.1.1`
- **Upstream:** [source repository](<https://github.com/bourumir-wyngs/rs-read-trimesh>) · [crates.io](<https://crates.io/crates/rs-read-trimesh>)
- **License:** MIT
- **Parsed scope:** ASCII PLY triangle mesh vertices and faces
- **Underlying family:** ply-rs-bw fork
- **Local input API:** `load_trimesh(path, scale)`
- **Documentation:** [API reference](<https://docs.rs/rs-read-trimesh/2.1.1/rs_read_trimesh/>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/rust/rs_read_trimesh/README.md)

```sh
python3 parsarium.py build ascii_ply rust rs_read_trimesh
python3 parsarium.py run ascii_ply rust rs_read_trimesh controls/ascii_ply/triangle.ply
```
