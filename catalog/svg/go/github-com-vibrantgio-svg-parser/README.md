# github.com/vibrantgio/svg/parser — SVG / Go

- **Pinned release:** `v0.1.3`
- **License:** BSD-3-Clause
- **Parsed scope:** paths, width
- **Underlying family:** oksvg lineage
- **Local input API:** `NewParser(IgnoreErrorMode).ParseStream(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/vibrantgio/svg/parser@v0.1.3>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
