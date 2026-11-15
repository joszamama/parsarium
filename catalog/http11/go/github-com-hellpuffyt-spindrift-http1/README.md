# github.com/hellpuffyt/spindrift/http1 — HTTP/1.1 / Go

- **Pinned release:** `v0.0.0-20261022160824-5a92c9177f42`
- **License:** MIT
- **Parsed scope:** request message
- **Underlying family:** spindrift HTTP/1 parser
- **Local input API:** `ReadRequest(*bufio.Reader, Limits)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/hellpuffyt/spindrift/http1>)
- **Catalog evidence:** [parser record](../../../../data/go/http11/parsers.json) · [control verification](../../../../data/go/http11/verification.json) · [within-ecosystem ranking](../../../../data/go/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "proto": "HTTP/1.1"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
