# sply — ASCII PLY / C

- **Pinned release:** `1.2.0`
- **License:** MIT
- **Parsed scope:** three vertex callbacks and one parsed triangle face with indices
- **Underlying family:** SPly fork of RPly ANSI C parser
- **Local input API:** `ply_open(local ASCII PLY filename); ply_read_header; ply_set_read_cb; ply_read`
- **Documentation:** [API reference](<https://github.com/Anteru/sply/blob/1.2.0/Readme.md>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "face": [
    0,
    1,
    2
  ]
}
```

SPly 1.2.0 is a separately tagged MIT library package with custom-I/O and locale changes, fully compatible with RPly; shares the RPly parser lineage and C callback API.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
