# github.com/evanphx/wildcat — HTTP/1.1 / Go

- **Pinned release:** `v0.0.0-20141114174135-e7012f664567`
- **License:** BSD-2-Clause
- **Parsed scope:** request head
- **Underlying family:** wildcat HTTP parser
- **Local input API:** `HTTPParser.Parse([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/evanphx/wildcat@v0.0.0-20141114174135-e7012f664567>)
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
