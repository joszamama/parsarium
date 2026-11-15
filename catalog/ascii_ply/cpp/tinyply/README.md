# tinyply — ASCII PLY / C++

- **Pinned release:** `3.0`
- **License:** Public-Domain
- **Parsed scope:** three parsed vertices and one triangular face from ASCII PLY
- **Underlying family:** tinyply header-only PLY parser
- **Local input API:** `std::ifstream(local filename); tinyply::PlyFile::parse_header/request_properties_from_element/read`
- **Documentation:** [API reference](<https://github.com/ddiakopoulos/tinyply/blob/3.0/README.md>)
- **Catalog evidence:** [parser record](../../../../data/cpp/ascii_ply/parsers.json) · [control verification](../../../../data/cpp/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/cpp/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1
}
```

Independent header-only C++ PLY parser, not an alias of Assimp or OpenMesh.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
