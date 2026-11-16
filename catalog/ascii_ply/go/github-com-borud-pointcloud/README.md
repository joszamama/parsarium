# github.com/borud/pointcloud — ASCII PLY / Go

- **Pinned release:** `v0.6.1`
- **License:** Apache-2.0
- **Parsed scope:** ASCII PLY vertex count and coordinate bounds
- **Underlying family:** borud pointcloud PLY
- **Local input API:** `ReadPLY(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/borud/pointcloud@v0.6.1>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_ply/parsers.json) · [control verification](../../../../data/go/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "bounds": [
    0,
    1,
    0,
    1
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/go/github_com_borud_pointcloud/README.md)

```sh
python3 parsarium.py build ascii_ply go github_com_borud_pointcloud
python3 parsarium.py run ascii_ply go github_com_borud_pointcloud controls/ascii_ply/triangle.ply
```
