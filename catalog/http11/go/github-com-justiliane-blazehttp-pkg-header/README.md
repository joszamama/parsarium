# github.com/justIliane/blazehttp/pkg/header — HTTP/1.1 / Go

- **Pinned release:** `v1.0.0`
- **License:** MIT
- **Parsed scope:** request header
- **Underlying family:** blazehttp header parser
- **Local input API:** `Parse([]byte, *ParsedRequest)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/justIliane/blazehttp/pkg/header@v1.0.0>)
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

[Docker harness and verification receipt](../../../../projects/http11/go/github_com_justiliane_blazehttp_pkg_header/README.md)

```sh
python3 parsarium.py build http11 go github_com_justiliane_blazehttp_pkg_header
python3 parsarium.py run http11 go github_com_justiliane_blazehttp_pkg_header controls/http11/request.http
```
