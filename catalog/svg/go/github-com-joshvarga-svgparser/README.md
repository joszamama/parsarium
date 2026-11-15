# github.com/JoshVarga/svgparser — SVG / Go

- **Pinned release:** `v0.0.0-20200804023048-5eaba627a7d1`
- **License:** MIT
- **Parsed scope:** rects, root
- **Underlying family:** JoshVarga SVG tree parser
- **Local input API:** `Parse(io.Reader, true).FindAll(rect)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/JoshVarga/svgparser@v0.0.0-20200804023048-5eaba627a7d1>)
- **Catalog evidence:** [parser record](../../../../data/go/svg/parsers.json) · [control verification](../../../../data/go/svg/verification.json) · [within-ecosystem ranking](../../../../data/go/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "rects": 2,
  "root": "svg"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
