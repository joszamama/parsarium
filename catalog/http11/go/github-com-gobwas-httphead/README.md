# github.com/gobwas/httphead — HTTP/1.1 / Go

- **Pinned release:** `v0.1.0`
- **License:** MIT
- **Parsed scope:** request line only
- **Underlying family:** gobwas HTTP request-line parser
- **Local input API:** `ParseRequestLine([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/gobwas/httphead@v0.1.0>)
- **Catalog evidence:** [parser record](../../../../data/go/http11/parsers.json) · [control verification](../../../../data/go/http11/verification.json) · [within-ecosystem ranking](../../../../data/go/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "major": 1,
  "minor": 1
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
