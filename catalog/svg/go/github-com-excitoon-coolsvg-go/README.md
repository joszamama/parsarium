# github.com/excitoon/coolsvg-go — SVG / Go

- **Pinned release:** `v0.0.0-20260812001811-a8ecd1868275`
- **License:** MIT
- **Parsed scope:** green, red, width
- **Underlying family:** oksvg lineage
- **Local input API:** `ReadIconStream(io.Reader).Render(image.RGBA)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/excitoon/coolsvg-go@v0.0.0-20260812001811-a8ecd1868275>)
- **Catalog evidence:** [parser record](../../../../data/go/svg/parsers.json) · [control verification](../../../../data/go/svg/verification.json) · [within-ecosystem ranking](../../../../data/go/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "green": 255,
  "red": 255,
  "width": 2
}
```

Shared code lineage; package count does not imply independent SVG parser engines.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
