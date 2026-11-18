# github.com/bloeys/assimp-go/asig — ASCII PLY / Go

- **Pinned release:** `v0.6.0`
- **Upstream:** [source repository](<https://github.com/bloeys/assimp-go>) · [pkg.go.dev](<https://pkg.go.dev/github.com/bloeys/assimp-go/asig>)
- **License:** MIT
- **Parsed scope:** ASCII PLY mesh, vertex, and face counts
- **Underlying family:** Assimp C++ importer
- **Local input API:** `ImportFile(string, PostProcess)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/bloeys/assimp-go@v0.6.0/asig>)
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

Go wrapper or fork over Assimp; package count does not imply independent parser engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/go/github_com_bloeys_assimp_go_asig/README.md)

```sh
python3 parsarium.py build ascii_ply go github_com_bloeys_assimp_go_asig
python3 parsarium.py run ascii_ply go github_com_bloeys_assimp_go_asig controls/ascii_ply/triangle.ply
```
