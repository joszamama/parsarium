# github.com/lesismal/fib/http — HTTP/1.1 / Go

- **Pinned release:** `v1.5.6`
- **License:** MIT
- **Parsed scope:** request message
- **Underlying family:** fib HTTP parser
- **Local input API:** `Parser.Feed([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/lesismal/fib/http@v1.5.6>)
- **Catalog evidence:** [parser record](../../../../data/go/http11/parsers.json) · [control verification](../../../../data/go/http11/verification.json) · [within-ecosystem ranking](../../../../data/go/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "host": "example.test",
  "proto": "HTTP/1.1"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
