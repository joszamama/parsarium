# pdal_c — ASCII PLY / C

- **Pinned release:** `2.2.3`
- **License:** BSD-3-Clause
- **Parsed scope:** ASCII PLY point-cloud subset: three parsed points through explicit readers.ply stage; no mesh exposed in this view
- **Underlying family:** PDAL native PLY reader via pdal-c C API
- **Local input API:** `PDALCreatePipeline(JSON readers.ply with local filename); PDALExecutePipeline; PDALGetPointViews; PDALGetPointViewSize`
- **Documentation:** [API reference](<https://github.com/PDAL/CAPI/blob/v2.2.3/README.md>)
- **Catalog evidence:** [parser record](../../../../data/c/ascii_ply/parsers.json) · [control verification](../../../../data/c/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/c/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "points": 3,
  "view_points": 3,
  "triangles": 0
}
```

pdal-c is a separately released BSD-3-Clause C API wrapper over PDAL 2.10.2. The underlying syntax parser is PDAL readers.ply; do not count it as an independent engine from PDAL.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
