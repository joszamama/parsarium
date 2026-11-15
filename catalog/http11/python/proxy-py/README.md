# proxy.py — HTTP/1.1 / Python

- **Pinned release:** `2.4.10`
- **License:** BSD-3-Clause
- **Parsed scope:** HTTP/1.1 request head
- **Underlying family:** proxy.py Python HTTP parser
- **Local input API:** `proxy.http.parser.HttpParser.request(bytes)`
- **Documentation:** [API reference](<https://proxypy.readthedocs.io/en/latest/pkg/proxy.http.parser/>)
- **Catalog evidence:** [parser record](../../../../data/python/http11/parsers.json) · [control verification](../../../../data/python/http11/verification.json) · [within-ecosystem ranking](../../../../data/python/http11/ranking.md)
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
