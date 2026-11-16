# github.com/go-fasthttp/fasthttp — HTTP/1.1 / Go

- **Pinned release:** `v0.0.0-20161128095036-1c39678a4dd0`
- **License:** MIT
- **Parsed scope:** request message
- **Underlying family:** fasthttp HTTP/1 parser
- **Local input API:** `Request.Read(*bufio.Reader)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/go-fasthttp/fasthttp@v0.0.0-20161128095036-1c39678a4dd0>)
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

[Docker harness and verification receipt](../../../../projects/http11/go/github_com_go_fasthttp_fasthttp/README.md)

```sh
python3 parsarium.py build http11 go github_com_go_fasthttp_fasthttp
python3 parsarium.py run http11 go github_com_go_fasthttp_fasthttp controls/http11/request.http
```
