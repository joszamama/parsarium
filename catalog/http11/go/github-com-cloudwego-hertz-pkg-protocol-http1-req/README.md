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

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/go/github_com_cloudwego_hertz_pkg_protocol_http1_req/README.md)

```sh
python3 parsarium.py build http11 go github_com_cloudwego_hertz_pkg_protocol_http1_req
python3 parsarium.py run http11 go github_com_cloudwego_hertz_pkg_protocol_http1_req controls/http11/request.http
```
