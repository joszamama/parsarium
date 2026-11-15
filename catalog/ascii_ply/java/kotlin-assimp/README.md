# kotlin-assimp — ASCII PLY / Java

- **Pinned release:** `v4.0`
- **License:** BSD-3-Clause
- **Parsed scope:** ASCII PLY triangle, three vertices, one face, parsed indices [0,1,2]
- **Underlying family:** Kotlin-graphics JVM Assimp port PLY importer
- **Local input API:** `new Importer().readFile(local File.toURI(), 0) -> AiScene with AiMesh vertices/faces`
- **Documentation:** [API reference](<https://github.com/kotlin-graphics/assimp/tree/v4.0#code>)
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

Pure JVM port of native Assimp with its own Kotlin PlyLoader and PlyParser; derived parser lineage is recorded separately from the existing LWJGL/native Assimp wrappers.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
