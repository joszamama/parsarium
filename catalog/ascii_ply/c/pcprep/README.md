# pcprep — ASCII PLY / C

- **Pinned release:** `pcprep-v1.0`
- **License:** MIT
- **Parsed scope:** Three parsed point coordinates from one valid ASCII PLY triangle; no face data exposed by this API
- **Underlying family:** pcprep C facade over bundled miniply C++ PLYReader
- **Local input API:** `pointcloud_load(pointcloud_t *, local PLY filename) returns success; cloud.size and cloud.pos contain parsed points`
- **Documentation:** [API reference](<https://github.com/filrg/pcprep/blob/pcprep-v1.0/include/pcprep/pointcloud.h>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "second_x": 1.0
}
```

A distinct released C library package from filrg. It shares bundled miniply C++ parsing with PCC and separately recorded Python paths. The exact GitHub release tag is pcprep-v1.0, while its CMake version is 1.0.1.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
