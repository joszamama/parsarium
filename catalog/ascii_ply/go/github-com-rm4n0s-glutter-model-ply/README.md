# github.com/rm4n0s/glutter/model/ply — ASCII PLY / Go

- **Pinned release:** `v1.17.0`
- **License:** BSD-3-Clause
- **Parsed scope:** ASCII PLY mesh and face counts
- **Underlying family:** glutter PLY
- **Local input API:** `Decode(context.Context, io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/rm4n0s/glutter@v1.17.0/model/ply>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_ply/parsers.json) · [control verification](../../../../data/go/ascii_ply/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_ply/ranking.md)
- **Valid control:** [`controls/ascii_ply/triangle.ply`](../../../../controls/ascii_ply/triangle.ply)

## Observed control result

```json
{
  "meshes": 1,
  "faces": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_ply/go/github_com_rm4n0s_glutter_model_ply/README.md)

```sh
python3 parsarium.py build ascii_ply go github_com_rm4n0s_glutter_model_ply
python3 parsarium.py run ascii_ply go github_com_rm4n0s_glutter_model_ply controls/ascii_ply/triangle.ply
```
