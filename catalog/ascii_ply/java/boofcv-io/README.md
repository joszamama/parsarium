# boofcv-io — ASCII PLY / Java

- **Pinned release:** `1.6.0`
- **License:** Apache-2.0
- **Parsed scope:** ASCII triangle, three vertices, one face, parsed indices [0,1,2]
- **Underlying family:** BoofCV native Java PLY mesh reader
- **Local input API:** `PointCloudIO.load(PointCloudIO.Format.PLY, InputStream from local file, VertexMesh)`
- **Documentation:** [API reference](<https://boofcv.org/index.php?title=Example_Load_and_Save_Point_Clouds>)
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

Public BoofCV mesh API dispatches to its own PlyCodec and PlyReader, with no shared syntax reader found among the other included Java paths.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
