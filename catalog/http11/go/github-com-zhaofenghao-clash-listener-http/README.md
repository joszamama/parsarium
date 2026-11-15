# github.com/zhaofenghao/clash/listener/http — HTTP/1.1 / Go

- **Pinned release:** `v1.0.14`
- **License:** GPL-3.0
- **Parsed scope:** request message
- **Underlying family:** Go net/http fork or wrapper
- **Local input API:** `ReadRequest(*bufio.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/zhaofenghao/clash/listener/http@v1.0.14>)
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

This package shares a parser family or code lineage with another row; package paths do not imply independent engines.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
