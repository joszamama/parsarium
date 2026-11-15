# jmist-core — ASCII PLY / Java

- **Pinned release:** `0.1.3`
- **License:** MIT
- **Parsed scope:** ASCII triangle, three vertices, one face, vertex X value and face indices
- **Underlying family:** JMIST native Java PLY event reader
- **Local input API:** `new PlyReader().read(File local path, PlyTarget); ElementListener receives parsed vertex and face properties`
- **Documentation:** [API reference](<https://github.com/bwkimmel/jmist/blob/v0.1.3/jmist-core/src/main/java/ca/eandb/jmist/framework/loader/ply/PlyReader.java>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_ply/parsers.json) · [control verification](../../../../data/java/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1,
  "second_x": 1.0,
  "indices": [
    0,
    1,
    2
  ]
}
```

Tagged Java source implements its own PLY header and property reader with callbacks; no shared syntax parser with the other included Java paths was found.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
