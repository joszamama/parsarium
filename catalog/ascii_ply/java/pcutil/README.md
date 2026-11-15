# pcutil — ASCII PLY / Java

- **Pinned release:** `0.3.0`
- **License:** MIT
- **Parsed scope:** ASCII PLY triangle vertex and face lists, parsed face indices
- **Underlying family:** PointCloudUtilities annotated PLY reader
- **Local input API:** `new PlyReader().read(File local path, annotated PointCloud.class)`
- **Documentation:** [API reference](<https://github.com/zhoujianling/PointCloudUtilities#plyreader>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_ply/parsers.json) · [control verification](../../../../data/java/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "indices": [
    0,
    1,
    2
  ]
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
