# github.com/nelthaarion/breeze — HTTP/1.1 / Go

- **Pinned release:** `v1.6.2`
- **License:** MIT
- **Parsed scope:** request message
- **Underlying family:** breeze HTTP parser
- **Local input API:** `ParseHTTPRequest([]byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/nelthaarion/breeze@v1.6.2>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/go/github_com_nelthaarion_breeze/README.md)

```sh
python3 parsarium.py build http11 go github_com_nelthaarion_breeze
python3 parsarium.py run http11 go github_com_nelthaarion_breeze controls/http11/request.http
```
