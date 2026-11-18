# github.com/lemon4ksan/mach/server/h1 — HTTP/1.1 / Go

- **Pinned release:** `v0.2.0`
- **Upstream:** [source repository](<https://github.com/Lemon4ksan/mach>) · [pkg.go.dev](<https://pkg.go.dev/github.com/lemon4ksan/mach/server/h1>)
- **License:** BSD-3-Clause
- **Parsed scope:** request message
- **Underlying family:** mach H1 parser
- **Local input API:** `Request.ReadRequest(*bufio.Reader, *ByteBuffer, int64)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/lemon4ksan/mach/server/h1@v0.2.0>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/go/github_com_lemon4ksan_mach_server_h1/README.md)

```sh
python3 parsarium.py build http11 go github_com_lemon4ksan_mach_server_h1
python3 parsarium.py run http11 go github_com_lemon4ksan_mach_server_h1 controls/http11/request.http
```
