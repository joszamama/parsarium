# nimbleterminal.dev/nt3d/mesh — ASCII PLY / Go

- **Pinned release:** `v0.8.1`
- **License:** MIT
- **Parsed scope:** ASCII PLY object and triangle counts
- **Underlying family:** nt3d PLY
- **Local input API:** `DecodePLY([]byte, *Options)`
- **Documentation:** [API reference](<https://pkg.go.dev/nimbleterminal.dev/nt3d@v0.8.1/mesh>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_ply/parsers.json) · [control verification](../../../../data/go/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "objects": 1,
  "faces": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/go/nimbleterminal_dev_nt3d_mesh/README.md)

```sh
python3 parsarium.py build ascii_ply go nimbleterminal_dev_nt3d_mesh
python3 parsarium.py run ascii_ply go nimbleterminal_dev_nt3d_mesh controls/ascii_ply/triangle.ply
```
