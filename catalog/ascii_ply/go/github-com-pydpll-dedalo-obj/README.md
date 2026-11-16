# github.com/pydpll/dedalo/obj — ASCII PLY / Go

- **Pinned release:** `v0.0.0-20260811120505-e095fa690fcf`
- **License:** MIT
- **Parsed scope:** ASCII PLY vertex and face counts
- **Underlying family:** dedalo PLY
- **Local input API:** `ParsePLY(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/pydpll/dedalo@v0.0.0-20260811120505-e095fa690fcf/obj>)
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

[Docker harness and verification receipt](../../../../projects/ascii_ply/go/github_com_pydpll_dedalo_obj/README.md)

```sh
python3 parsarium.py build ascii_ply go github_com_pydpll_dedalo_obj
python3 parsarium.py run ascii_ply go github_com_pydpll_dedalo_obj controls/ascii_ply/triangle.ply
```
