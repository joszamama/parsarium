# ply-rs — ASCII PLY / Rust

- **Pinned release:** `0.1.3`
- **License:** MIT
- **Parsed scope:** complete ASCII PLY: header, vertices, faces
- **Underlying family:** ply-rs lineage
- **Local input API:** `Parser::<DefaultElement>::read_ply(&mut Cursor<&[u8]>)`
- **Documentation:** [API reference](<https://docs.rs/ply-rs/0.1.3/ply_rs/>)
- **Catalog evidence:** [parser record](../../../../data/rust/ascii_ply/parsers.json) · [control verification](../../../../data/rust/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/rust/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "format": "Ascii"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/rust/ply_rs/README.md)

```sh
python3 parsarium.py build ascii_ply rust ply_rs
python3 parsarium.py run ascii_ply rust ply_rs controls/ascii_ply/triangle.ply
```
