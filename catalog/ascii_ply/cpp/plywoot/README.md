# plywoot — ASCII PLY / C++

- **Pinned release:** `0.3.0`
- **License:** GPL-3.0-or-later
- **Parsed scope:** three parsed vertices and one triangle with three indices
- **Underlying family:** PLYwoot native ASCII parser
- **Local input API:** `std::ifstream(local filename); plywoot::IStream(stream); readElement<Vertex, Layout>(); readElement<Triangle, Layout>()`
- **Documentation:** [API reference](<https://github.com/ton/PLYwoot/blob/v0.3.0/README.md>)
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

Independent header-only C++ PLY parser with direct stream input.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
