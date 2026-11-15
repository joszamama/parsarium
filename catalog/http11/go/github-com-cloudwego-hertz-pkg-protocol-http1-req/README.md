# github.com/cloudwego/hertz/pkg/protocol/http1/req — HTTP/1.1 / Go

- **Pinned release:** `v0.10.6`
- **License:** Apache-2.0
- **Parsed scope:** request message
- **Underlying family:** Hertz / fasthttp lineage
- **Local input API:** `Read(*Request, network.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/cloudwego/hertz/pkg/protocol/http1/req@v0.10.6>)
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
