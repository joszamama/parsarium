# github.com/tdewolff/minify/v2/svg — SVG / Go

- **Pinned release:** `v2.24.25`
- **License:** MIT
- **Parsed scope:** SVG-aware transformed colors and markup
- **Underlying family:** tdewolff SVG minifier
- **Local input API:** `Minify(*minify.M, io.Writer, io.Reader, params)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/tdewolff/minify/v2/svg@v2.24.25>)
- **Catalog evidence:** [parser record](../../../../data/go/svg/parsers.json) · [control verification](../../../../data/go/svg/verification.json) · [within-ecosystem ranking](../../../../data/go/svg/ranking.md)
- **Valid control:** [`controls/svg/red-green.svg`](../../../../controls/svg/red-green.svg)

## Observed control result

```json
{
  "minified": "<svg xmlns=\"http://www.w3.org/2000/svg\" width=\"2\" height=\"1\" viewBox=\"0 0 2 1\"><rect x=\"0\" y=\"0\" width=\"1\" height=\"1\" fill=\"red\"/><rect x=\"1\" y=\"0\" width=\"1\" height=\"1\" fill=\"#0f0\"/></svg>"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
