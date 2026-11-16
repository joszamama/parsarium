# github.com/NimbleMarkets/oksvg — SVG / Go

- **Pinned release:** `v0.1.6`
- **License:** BSD-3-Clause
- **Parsed scope:** paths, width
- **Underlying family:** oksvg lineage
- **Local input API:** `ReadIconStream(io.Reader).ViewBox, SVGPaths`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/NimbleMarkets/oksvg@v0.1.6>)
- **Catalog evidence:** [parser record](../../../../data/go/svg/parsers.json) · [control verification](../../../../data/go/svg/verification.json) · [within-ecosystem ranking](../../../../data/go/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "paths": 2,
  "width": 2
}
```

Shared code lineage; package count does not imply independent SVG parser engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/go/github_com_nimblemarkets_oksvg/README.md)

```sh
python3 parsarium.py build svg go github_com_nimblemarkets_oksvg
python3 parsarium.py run svg go github_com_nimblemarkets_oksvg controls/svg/red-green.svg
```
