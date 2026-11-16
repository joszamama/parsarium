# github.com/projectdiscovery/nuclei/v3/pkg/protocols/http/raw — HTTP/1.1 / Go

- **Pinned release:** `v3.11.1`
- **License:** MIT
- **Parsed scope:** raw request message
- **Underlying family:** nuclei raw HTTP parser
- **Local input API:** `ParseRawRequest(string, bool)`
- **Documentation:** [API reference](<https://pkg.go.dev/github.com/projectdiscovery/nuclei/v3/pkg/protocols/http/raw@v3.11.1>)
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

[Docker harness and verification receipt](../../../../projects/http11/go/github_com_projectdiscovery_nuclei_v3_pkg_protocols_http_raw/README.md)

```sh
python3 parsarium.py build http11 go github_com_projectdiscovery_nuclei_v3_pkg_protocols_http_raw
python3 parsarium.py run http11 go github_com_projectdiscovery_nuclei_v3_pkg_protocols_http_raw controls/http11/request.http
```
