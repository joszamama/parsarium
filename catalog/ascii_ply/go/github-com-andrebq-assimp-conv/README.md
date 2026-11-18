# github.com/andrebq/assimp/conv — ASCII PLY / Go

- **Pinned release:** `v0.0.0-20121130215243-a775ba6866d8`
- **License:** MIT
- **Parsed scope:** ASCII PLY mesh, vertex, and face counts
- **Underlying family:** Assimp C++ importer
- **Local input API:** `conv.LoadAsset(path string) (*assimp.Scene, error)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/andrebq/assimp@v0.0.0-20121130215243-a775ba6866d8/conv#LoadAsset>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_ply/parsers.json) · [control verification](../../../../data/go/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "meshes": 1,
  "vertices": 3,
  "faces": 1
}
```

Go wrapper over Assimp (cgo, pkg-config assimp): LoadAsset calls aiImportFile through its own C helpers (aiw_*.c) and converts vertices, normals, colours, UVs and faces to Go structs. Fourth path of the Assimp family after tbogdala/assimp-go, bloeys/assimp-go and rishabh-bector/assimp-golang; its 2012 binding code is its own, but the PLY text is parsed by the same Assimp PLY importer (Debian libassimp5 in the image), so the package count does not imply an independent parser engine. No tagged release (pinned pseudo-version, 2012-11-30). Found through a pkg.go.dev package search ('assimp').

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/go/github_com_andrebq_assimp_conv/README.md)

```sh
python3 parsarium.py build ascii_ply go github_com_andrebq_assimp_conv
python3 parsarium.py run ascii_ply go github_com_andrebq_assimp_conv controls/ascii_ply/triangle.ply
```
