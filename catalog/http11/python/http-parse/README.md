# http-parse — HTTP/1.1 / Python

- **Pinned release:** `0.1.5`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 request method, target and Host
- **Underlying family:** http-parse Python parser
- **Local input API:** `http_parse.parse(raw_request_str)`
- **Documentation:** [API reference](<https://pypi.org/project/http-parse/0.1.5/>)
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
