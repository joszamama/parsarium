# github.com/meta-apex/metarpc/codec/http — HTTP/1.1 / Go

- **Pinned release:** `v0.0.0-20250816075809-78e603aff299`
- **License:** Apache-2.0
- **Parsed scope:** request message
- **Underlying family:** fasthttp-derived metarpc parser
- **Local input API:** `Parser.Parse([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/meta-apex/metarpc/codec/http@v0.0.0-20250816075809-78e603aff299>)
- **Catalog evidence:** [parser record](../../../../data/go/http11/parsers.json) · [control verification](../../../../data/go/http11/verification.json) · [within-ecosystem ranking](../../../../data/go/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "host": "example.test"
}
```

This package shares a parser family or code lineage with another row; package paths do not imply independent engines.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
