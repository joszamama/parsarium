# github.com/openctemio/openctem/api/pkg/domain/evidence — HTTP/1.1 / Go

- **Pinned release:** `v0.0.0-20261107202920-27e7faec6f5d`
- **License:** GPL-3.0
- **Parsed scope:** raw request message
- **Underlying family:** openctem raw HTTP parser
- **Local input API:** `ParseRawRequest(string, string)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/openctemio/openctem/api/pkg/domain/evidence@v0.0.0-20261107202920-27e7faec6f5d>)
- **Catalog evidence:** [parser record](../../../../data/go/http11/parsers.json) · [control verification](../../../../data/go/http11/verification.json) · [within-ecosystem ranking](../../../../data/go/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "url": "http://example.test/parsarium?x=1",
  "proto": "HTTP/1.1"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
