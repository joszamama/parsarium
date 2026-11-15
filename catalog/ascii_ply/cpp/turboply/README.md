# turboply — ASCII PLY / C++

- **Pinned release:** `1.0.6`
- **License:** MIT
- **Parsed scope:** three parsed vertices and one face with three indices
- **Underlying family:** TurboPLY native reader
- **Local input API:** `PlyFileReader(local filename); parseHeader; bind_reader(VertexSpec, FaceSpec)`
- **Documentation:** [API reference](<https://github.com/guangxi-research/turboply/blob/v1.0.6/README.md>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_ply/parsers.json) · [control verification](../../../../data/cpp/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_ply/ranking.md)
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

Independent C++20 PLY parser; compatibility build patch changes declaration order only.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
