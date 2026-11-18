# github.com/lafriks/go-svg — SVG / Go

- **Pinned release:** `v0.5.1`
- **Upstream:** [source repository](<https://github.com/lafriks/go-svg>) · [pkg.go.dev](<https://pkg.go.dev/github.com/lafriks/go-svg>)
- **License:** BSD-3-Clause
- **Parsed scope:** paths, width
- **Underlying family:** oksvg lineage
- **Local input API:** `Parse(io.Reader, IgnoreErrorMode).SvgPaths`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/lafriks/go-svg@v0.5.1>)
- **Catalog evidence:** [parser record](../../../../data/go/svg/parsers.json) · [control verification](../../../../data/go/svg/verification.json) · [within-ecosystem ranking](../../../../data/go/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "paths": 2,
  "width": "2"
}
```

Shared code lineage; package count does not imply independent SVG parser engines.

## Run this target

[Docker harness and verification receipt](../../../../projects/svg/go/github_com_lafriks_go_svg/README.md)

```sh
python3 parsarium.py build svg go github_com_lafriks_go_svg
python3 parsarium.py run svg go github_com_lafriks_go_svg controls/svg/red-green.svg
```
