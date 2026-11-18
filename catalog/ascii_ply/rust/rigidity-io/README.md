# rigidity-io — ASCII PLY / Rust

- **Pinned release:** `0.2.0`
- **Upstream:** [source repository](<https://github.com/Dmitrii173173/rigidity>) · [crates.io](<https://crates.io/crates/rigidity-io>)
- **License:** AGPL-3.0-only
- **Parsed scope:** ASCII PLY vertex cloud; faces not interpreted
- **Underlying family:** rigidity-io PLY reader
- **Local input API:** `read_ply(path)`
- **Documentation:** [API reference](<https://docs.rs/rigidity-io/0.2.0/rigidity_io/>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_ply/parsers.json) · [control verification](../../../../data/rust/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/rust/rigidity_io/README.md)

```sh
python3 parsarium.py build ascii_ply rust rigidity_io
python3 parsarium.py run ascii_ply rust rigidity_io controls/ascii_ply/triangle.ply
```
