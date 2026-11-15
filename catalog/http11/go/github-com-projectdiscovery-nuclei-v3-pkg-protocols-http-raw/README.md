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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
