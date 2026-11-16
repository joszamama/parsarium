# github.com/zhaofenghao/clash/listener/http — HTTP/1.1 / Go

- **Pinned release:** `v1.0.14`
- **License:** GPL-3.0
- **Parsed scope:** request message
- **Underlying family:** Go net/http stdlib parser exposed through Clash linkname alias
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

Clash v1.0.14 declares ReadRequest with //go:linkname to net/http.readRequest; the package API executes the Go runtime parser. Coverage and AFL++ feedback therefore target net/http source, and this row is not an independent parser engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/go/github_com_zhaofenghao_clash_listener_http/README.md)

```sh
python3 parsarium.py build http11 go github_com_zhaofenghao_clash_listener_http
python3 parsarium.py run http11 go github_com_zhaofenghao_clash_listener_http controls/http11/request.http
```
