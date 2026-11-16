# ferrum_cloud — ASCII PLY / Rust

- **Pinned release:** `0.1.0`
- **License:** MIT
- **Parsed scope:** ASCII PLY vertex cloud
- **Underlying family:** ferrum_cloud PLY reader
- **Local input API:** `io::load_ply(path)`
- **Documentation:** [API reference](<https://docs.rs/ferrum_cloud/0.1.0/ferrum_cloud/>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_ply/parsers.json) · [control verification](../../../../data/rust/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/rust/ferrum_cloud/README.md)

```sh
python3 parsarium.py build ascii_ply rust ferrum_cloud
python3 parsarium.py run ascii_ply rust ferrum_cloud controls/ascii_ply/triangle.ply
```
