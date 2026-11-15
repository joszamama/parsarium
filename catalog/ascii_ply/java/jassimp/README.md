# jassimp — ASCII PLY / Java

- **Pinned release:** `1.0.0`
- **License:** BSD-3-Clause
- **Parsed scope:** ASCII PLY triangle mesh, vertex count and face count
- **Underlying family:** JAssimp JNI binding over native Assimp PLY importer
- **Local input API:** `Jassimp.importFile(String local filename); AiScene.getMeshes(); AiMesh.getNumVertices() and getNumFaces()`
- **Documentation:** [API reference](<https://github.com/maeda6uiui/JAssimp/blob/v1.0.0/src/main/java/com/github/dabasan/jassimp/Jassimp.java>)
- **Catalog evidence:** [parser record](../../../../data/java/ascii_ply/parsers.json) · [control verification](../../../../data/java/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/java/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "meshes": 1,
  "vertices": 3,
  "faces": 1
}
```

Separately published Maven Java binding; JNI built from tagged source against pinned Assimp 6.0.6. Shares native Assimp PLY parser family with LWJGL Assimp, MonkeyWrench, and C/C++ Assimp call sites.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
