# github.com/ncruces/go-pnm — ASCII PNM / Go

- **Pinned release:** `v1.0.0`
- **License:** BSD-2-Clause
- **Parsed scope:** P3 pixels and dimensions
- **Underlying family:** gopnm lineage
- **Local input API:** `Decode(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/ncruces/go-pnm@v1.0.0>)
- **Catalog evidence:** [parser record](../../../../data/go/ascii_pnm/parsers.json) · [control verification](../../../../data/go/ascii_pnm/verification.json) · [within-ecosystem ranking](../../../../data/go/ascii_pnm/ranking.md)
- **Valid control:** [`controls/ascii_pnm/red-green.ppm`](../../../../controls/ascii_pnm/red-green.ppm)

## Observed control result

```json
{
  "height": 1,
  "rgb0": [
    255,
    0,
    0
  ],
  "rgb1": [
    0,
    255,
    0
  ],
  "width": 2
}
```

Shared code lineage or native parser; package count does not imply independent parser engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/ascii_pnm/go/github_com_ncruces_go_pnm/README.md)

```sh
python3 parsarium.py build ascii_pnm go github_com_ncruces_go_pnm
python3 parsarium.py run ascii_pnm go github_com_ncruces_go_pnm controls/ascii_pnm/red-green.ppm
```
