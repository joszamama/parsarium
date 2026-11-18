# cumulus3d-core — ASCII PLY / Rust

- **Pinned release:** `0.11.1`
- **Upstream:** [source repository](<https://github.com/AH100-1/cumulus3d>) · [crates.io](<https://crates.io/crates/cumulus3d-core>)
- **License:** Apache-2.0
- **Parsed scope:** ASCII PLY vertex cloud
- **Underlying family:** cumulus3d-core PLY reader
- **Local input API:** `io::read_ply(path)`
- **Documentation:** [API reference](<https://docs.rs/cumulus3d-core/0.11.1/cumulus3d_core/>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_ply/parsers.json) · [control verification](../../../../data/rust/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/rust/cumulus3d_core/README.md)

```sh
python3 parsarium.py build ascii_ply rust cumulus3d_core
python3 parsarium.py run ascii_ply rust cumulus3d_core controls/ascii_ply/triangle.ply
```
