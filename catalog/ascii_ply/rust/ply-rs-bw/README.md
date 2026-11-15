# ply-rs-bw — ASCII PLY / Rust

- **Pinned release:** `4.0.1`
- **License:** MIT
- **Parsed scope:** complete ASCII PLY: header, vertices, faces
- **Underlying family:** ply-rs fork
- **Local input API:** `Parser::<DefaultElement>::read_ply(&mut Cursor<&[u8]>)`
- **Documentation:** [API reference](<https://docs.rs/ply-rs-bw/4.0.1/ply_rs_bw/>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/rust/ply_rs_bw/README.md)

```sh
python3 parsarium.py build ascii_ply rust ply_rs_bw
python3 parsarium.py run ascii_ply rust ply_rs_bw controls/ascii_ply/triangle.ply
```
