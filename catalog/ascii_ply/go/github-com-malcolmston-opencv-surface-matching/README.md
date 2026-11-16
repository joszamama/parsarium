# github.com/malcolmston/opencv/surface_matching — ASCII PLY / Go

- **Pinned release:** `v0.8.0`
- **License:** MIT
- **Parsed scope:** ASCII PLY vertex count and coordinate
- **Underlying family:** surface_matching PLY
- **Local input API:** `LoadPLY(string)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/malcolmston/opencv@v0.8.0/surface_matching>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_ply/parsers.json) · [control verification](../../../../data/go/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "first": [
    0,
    0,
    0
  ]
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/go/github_com_malcolmston_opencv_surface_matching/README.md)

```sh
python3 parsarium.py build ascii_ply go github_com_malcolmston_opencv_surface_matching
python3 parsarium.py run ascii_ply go github_com_malcolmston_opencv_surface_matching controls/ascii_ply/triangle.ply
```
