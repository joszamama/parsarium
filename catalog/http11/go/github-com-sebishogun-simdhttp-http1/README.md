# github.com/sebishogun/simdhttp/http1 — HTTP/1.1 / Go

- **Pinned release:** `v0.0.0-20261007210108-01268e016029`
- **License:** MIT
- **Parsed scope:** request head
- **Underlying family:** simdhttp HTTP/1 parser
- **Local input API:** `Parse(*Request, []byte, Compatible)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/sebishogun/simdhttp/http1@v0.0.0-20261007210108-01268e016029>)
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

[Docker harness and verification receipt](../../../../projects/http11/go/github_com_sebishogun_simdhttp_http1/README.md)

```sh
python3 parsarium.py build http11 go github_com_sebishogun_simdhttp_http1
python3 parsarium.py run http11 go github_com_sebishogun_simdhttp_http1 controls/http11/request.http
```
