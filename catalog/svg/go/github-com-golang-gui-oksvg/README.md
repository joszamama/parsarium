# github.com/golang-gui/oksvg — SVG / Go

- **Pinned release:** `v0.1.0`
- **License:** BSD-3-Clause
- **Parsed scope:** paths, width
- **Underlying family:** oksvg lineage
- **Local input API:** `ReadIconStream(io.Reader).ViewBox, SVGPaths`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/golang-gui/oksvg@v0.1.0>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
