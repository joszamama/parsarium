# github.com/antlabs/fio/http — HTTP/1.1 / Go

- **Pinned release:** `v0.2.8`
- **License:** Apache-2.0
- **Parsed scope:** request message
- **Underlying family:** fio native HTTP parser
- **Local input API:** `Parser.Parse([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/antlabs/fio/http@v0.2.8>)
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
