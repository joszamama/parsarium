# github.com/chenzhekl/goply — ASCII PLY / Go

- **Pinned release:** `v0.0.0-20190930133256-258c2381defd`
- **Upstream:** [source repository](<https://github.com/chenzhekl/goply>) · [pkg.go.dev](<https://pkg.go.dev/github.com/chenzhekl/goply>)
- **License:** MIT
- **Parsed scope:** ASCII PLY vertex and face counts
- **Underlying family:** goply
- **Local input API:** `New(io.Reader); Elements(string)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/chenzhekl/goply@v0.0.0-20190930133256-258c2381defd>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/go/github_com_chenzhekl_goply/README.md)

```sh
python3 parsarium.py build ascii_ply go github_com_chenzhekl_goply
python3 parsarium.py run ascii_ply go github_com_chenzhekl_goply controls/ascii_ply/triangle.ply
```
