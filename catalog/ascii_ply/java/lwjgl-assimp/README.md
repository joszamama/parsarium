# lwjgl-assimp — ASCII PLY / Java

- **Pinned release:** `3.4.3`
- **Upstream:** [source repository](<https://github.com/LWJGL/lwjgl3>) · [Maven Central](<https://central.sonatype.com/artifact/org.lwjgl/lwjgl-assimp>)
- **License:** BSD-3-Clause
- **Parsed scope:** ASCII PLY triangle vertex and face counts, parsed face indices
- **Underlying family:** LWJGL Java binding over native Assimp PLY importer; same Assimp parser family as C++ path
- **Local input API:** `Assimp.aiImportFile(String local path, 0) with pinned macOS arm64 native artifact`
- **Documentation:** [API reference](<https://javadoc.lwjgl.org/org/lwjgl/assimp/Assimp.html>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/java/lwjgl_assimp/README.md)

```sh
python3 parsarium.py build ascii_ply java lwjgl_assimp
python3 parsarium.py run ascii_ply java lwjgl_assimp controls/ascii_ply/triangle.ply
```
