# github.com/pgavlin/svg2 — SVG / Go

- **Pinned release:** `v0.0.0-20210919231505-4ace7308edc1`
- **License:** MIT
- **Parsed scope:** height, width
- **Underlying family:** pgavlin SVG2 decoder
- **Local input API:** `DecodeConfig(io.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/pgavlin/svg2>)
- **Catalog evidence:** [parser record](../../../../data/go/svg/parsers.json) · [control verification](../../../../data/go/svg/verification.json) · [within-ecosystem ranking](../../../../data/go/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "height": 1,
  "width": 2
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
