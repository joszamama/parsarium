# github.com/thebanri/limoni/graphics — ASCII PLY / Go

- **Pinned release:** `v0.16.0`
- **Upstream:** [source repository](<https://github.com/thebanri/limoni>) · [pkg.go.dev](<https://pkg.go.dev/github.com/thebanri/limoni/graphics>)
- **License:** Apache-2.0
- **Parsed scope:** ASCII PLY vertex and face counts
- **Underlying family:** limoni PLY
- **Local input API:** `ParsePLY(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/thebanri/limoni@v0.16.0/graphics>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_ply/parsers.json) · [control verification](../../../../data/go/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "vertices": 3,
  "faces": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/go/github_com_thebanri_limoni_graphics/README.md)

```sh
python3 parsarium.py build ascii_ply go github_com_thebanri_limoni_graphics
python3 parsarium.py run ascii_ply go github_com_thebanri_limoni_graphics controls/ascii_ply/triangle.ply
```
