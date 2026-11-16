# github.com/FastTLS/oohttp — HTTP/1.1 / Go

- **Pinned release:** `v0.0.0-20261026180050-43186effd7f4`
- **License:** BSD-3-Clause
- **Parsed scope:** request message
- **Underlying family:** Go net/http fork
- **Local input API:** `ReadRequest(*bufio.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/FastTLS/oohttp@v0.0.0-20261026180050-43186effd7f4>)
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

[Docker harness and verification receipt](../../../../projects/http11/go/github_com_fasttls_oohttp/README.md)

```sh
python3 parsarium.py build http11 go github_com_fasttls_oohttp
python3 parsarium.py run http11 go github_com_fasttls_oohttp controls/http11/request.http
```
