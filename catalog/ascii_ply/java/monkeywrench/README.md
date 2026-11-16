# MonkeyWrench — ASCII PLY / Java

- **Pinned release:** `1.0.1`
- **License:** BSD-3-Clause
- **Parsed scope:** ASCII PLY triangle mesh vertex and triangle counts, parsed face indices
- **Underlying family:** MonkeyWrench wrapper over LWJGL Assimp native PLY importer; same Assimp parser family as LWJGL and C++ paths
- **Local input API:** `JMonkeyEngine AssetManager.registerLoader(LwjglAssetLoader.class, 'ply'); loadModel(LwjglAssetKey for local FileLocator path)`
- **Documentation:** [API reference](<https://github.com/stephengold/MonkeyWrench#how-to-add-monkeywrench-to-an-existing-project>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/java/monkeywrench/README.md)

```sh
python3 parsarium.py build ascii_ply java monkeywrench
python3 parsarium.py run ascii_ply java monkeywrench controls/ascii_ply/triangle.ply
```
