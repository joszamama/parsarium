# github.com/EliCDavis/polyform/formats/ply — ASCII PLY / Go

- **Pinned release:** `v0.44.0`
- **License:** MIT
- **Parsed scope:** ASCII PLY vertex and face counts
- **Underlying family:** polyform PLY
- **Local input API:** `ReadMesh(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/EliCDavis/polyform@v0.44.0/formats/ply>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/go/polyform_ply/README.md)

```sh
python3 parsarium.py build ascii_ply go polyform_ply
python3 parsarium.py run ascii_ply go polyform_ply controls/ascii_ply/triangle.ply
```
