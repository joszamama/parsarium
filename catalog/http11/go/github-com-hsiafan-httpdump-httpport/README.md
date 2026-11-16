# github.com/hsiafan/httpdump/httpport — HTTP/1.1 / Go

- **Pinned release:** `v0.0.0-20231019014708-4fd809447b59`
- **License:** BSD-2-Clause
- **Parsed scope:** request message
- **Underlying family:** Go net/http port
- **Local input API:** `ReadRequest(*bufio.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/hsiafan/httpdump/httpport@v0.0.0-20231019014708-4fd809447b59>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/go/github_com_hsiafan_httpdump_httpport/README.md)

```sh
python3 parsarium.py build http11 go github_com_hsiafan_httpdump_httpport
python3 parsarium.py run http11 go github_com_hsiafan_httpdump_httpport controls/http11/request.http
```
