# github.com/lesismal/nbio/nbhttp — HTTP/1.1 / Go

- **Pinned release:** `v1.7.1`
- **License:** MIT
- **Parsed scope:** request message
- **Underlying family:** nbio HTTP parser
- **Local input API:** `Parser.Parse([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/lesismal/nbio/nbhttp@v1.7.1>)
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
