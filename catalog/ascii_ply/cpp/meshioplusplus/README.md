# meshioplusplus — ASCII PLY / C++

- **Pinned release:** `20.0.0`
- **License:** MIT
- **Parsed scope:** three mesh vertices and one triangle face with parsed indices from ASCII PLY
- **Underlying family:** meshio++ native C++ PLY parser
- **Local input API:** `meshioplusplus::read_ply(local filename); Mesh::NumPoints; Mesh::CellRange/CellView::Conn`
- **Documentation:** [API reference](<https://github.com/loumalouomega/meshioplusplus/blob/v20.0.0/src/cpp/include/meshioplusplus/formats/ply.hpp>)
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

The tagged src/cpp/src/formats/ply.cpp implements PLY parsing directly. It is a separate package and underlying parser family from RPly, tinyply, hapPLY, and the other listed readers.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
