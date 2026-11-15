# sceneview-core — ASCII PLY / Java

- **Pinned release:** `4.69.5`
- **License:** Apache-2.0
- **Parsed scope:** ASCII PLY triangle vertices, triangulated face and parsed indices
- **Underlying family:** SceneView Core pure Kotlin PLY parser
- **Local input API:** `Files.readAllBytes(local path) passed to PlyLoader.parse(byte[], ThreeMfUnit, limits), returning PlyModel vertex count, triangle count and indices`
- **Documentation:** [API reference](<https://github.com/sceneview/sceneview/blob/v4.69.5/sceneview-core/src/commonMain/kotlin/io/github/sceneview/core/ply/PlyLoader.kt>)
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

The released JVM artifact exposes a callable Java bytecode API over SceneView Core’s pure Kotlin PLY reader. Project-wide interest does not measure PLY use.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
