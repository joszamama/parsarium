# github.com/antlabs/httparser — HTTP/1.1 / Go

- **Pinned release:** `v0.0.11`
- **License:** Apache-2.0
- **Parsed scope:** request message
- **Underlying family:** antlabs httparser
- **Local input API:** `Parser.Execute(*Setting, []byte)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/antlabs/httparser@v0.0.11>)
- **Catalog evidence:** [parser record](../../../../data/go/http11/parsers.json) · [control verification](../../../../data/go/http11/verification.json) · [within-ecosystem ranking](../../../../data/go/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "major": 1,
  "minor": 1
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/go/github_com_antlabs_httparser/README.md)

```sh
python3 parsarium.py build http11 go github_com_antlabs_httparser
python3 parsarium.py run http11 go github_com_antlabs_httparser controls/http11/request.http
```
