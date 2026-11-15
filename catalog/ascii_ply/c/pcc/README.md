# pcc — ASCII PLY / C

- **Pinned release:** `0.1.0`
- **License:** GPL-3.0
- **Parsed scope:** Three parsed point coordinates from one valid ASCII PLY triangle; face not exposed by point-cloud API
- **Underlying family:** PCC C facade over bundled miniply C++ PLYReader
- **Local input API:** `pcc_point_cloud_init; pcc_point_cloud_t.read_from_file(&cloud, local PLY path); cloud.positions and cloud.size`
- **Documentation:** [API reference](<https://github.com/filrg/pcc/blob/v0.1.0/include/pcc/point_cloud.h>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "second_x": 1.0
}
```

Distinct tagged GPL C API package. Its PLY syntax parsing delegates to bundled miniply C++ source. The unrelated codec source requires zstd.h even when USE_ZSTD=OFF, so the replay compiles only the unmodified local PLY call path. miniply also underlies separately recorded Python pyminiply and pyvista-miniply paths.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
