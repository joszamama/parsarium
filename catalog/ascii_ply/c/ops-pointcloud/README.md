# ops_pointcloud — ASCII PLY / C

- **Pinned release:** `2026.45.1`
- **License:** LGPL-3.0-or-later
- **Parsed scope:** ASCII PLY point cloud subset: three parsed vertex coordinates; faces are not exposed by the point-cloud API
- **Underlying family:** Open Pointcloud Studio native Rust PLY reader through ops_pointcloud C ABI
- **Local input API:** `ops_cloud_open(local .ply path); ops_cloud_info; ops_cloud_read(points callback)`
- **Documentation:** [API reference](<https://github.com/OpenAEC-Foundation/open-pointcloud-studio/blob/v2026.45.1/docs/library.md>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "points": 3,
  "second_x": 1.0,
  "last_y": 1.0
}
```

One LGPL point-cloud core with C ABI; distinct package and syntax reader from the other C PLY paths. The local C adapter uses the official released SDK binary.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
