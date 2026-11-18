# github.com/rishabh-bector/assimp-golang — ASCII PLY / Go

- **Pinned release:** `v0.0.0-20190130041627-cbac4dcfdaf3`
- **Upstream:** [source repository](<https://github.com/rishabh-bector/assimp-golang>) · [pkg.go.dev](<https://pkg.go.dev/github.com/rishabh-bector/assimp-golang>)
- **License:** MIT
- **Parsed scope:** ASCII PLY mesh, vertex, and face counts
- **Underlying family:** Assimp C++ importer
- **Local input API:** `ImportFileFromMemory([]byte, uint, string)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/rishabh-bector/assimp-golang@v0.0.0-20190130041627-cbac4dcfdaf3>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/go/github_com_rishabh_bector_assimp_golang/README.md)

```sh
python3 parsarium.py build ascii_ply go github_com_rishabh_bector_assimp_golang
python3 parsarium.py run ascii_ply go github_com_rishabh_bector_assimp_golang controls/ascii_ply/triangle.ply
```
