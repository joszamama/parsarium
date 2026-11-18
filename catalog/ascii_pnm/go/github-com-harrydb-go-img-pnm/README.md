# github.com/harrydb/go/img/pnm — ASCII PNM / Go

- **Pinned release:** `v0.0.0-20160105214235-0ff7a05d1aa4`
- **Upstream:** [source repository](<https://github.com/harrydb/go>) · [pkg.go.dev](<https://pkg.go.dev/github.com/harrydb/go/img/pnm>)
- **License:** BSD-2-Clause
- **Parsed scope:** P3 pixels and dimensions
- **Underlying family:** peterh/go PNM lineage
- **Local input API:** `Decode(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/harrydb/go/img/pnm@v0.0.0-20160105214235-0ff7a05d1aa4>)
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

[Docker harness and verification receipt](../../../../projects/ascii_pnm/go/github_com_harrydb_go_img_pnm/README.md)

```sh
python3 parsarium.py build ascii_pnm go github_com_harrydb_go_img_pnm
python3 parsarium.py run ascii_pnm go github_com_harrydb_go_img_pnm controls/ascii_pnm/red-green.ppm
```
