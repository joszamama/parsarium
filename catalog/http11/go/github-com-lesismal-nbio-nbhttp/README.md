# github.com/lesismal/nbio/nbhttp — HTTP/1.1 / Go

- **Pinned release:** `v1.7.1`
- **Upstream:** [source repository](<https://github.com/lesismal/nbio>) · [pkg.go.dev](<https://pkg.go.dev/github.com/lesismal/nbio/nbhttp>)
- **License:** MIT
- **Parsed scope:** request message
- **Underlying family:** nbio HTTP parser
- **Local input API:** `Parser.Parse([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/lesismal/nbio/nbhttp@v1.7.1>)
- **Catalog evidence:** [parser record](../../../../data/go/http11/parsers.json) · [control verification](../../../../data/go/http11/verification.json) · [within-ecosystem ranking](../../../../data/go/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "proto": "HTTP/1.1"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/go/github_com_lesismal_nbio_nbhttp/README.md)

```sh
python3 parsarium.py build http11 go github_com_lesismal_nbio_nbhttp
python3 parsarium.py run http11 go github_com_lesismal_nbio_nbhttp controls/http11/request.http
```
