# http-parser — HTTP/1.1 / Python

- **Pinned release:** `0.9.0`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 request head
- **Underlying family:** node http-parser C binding
- **Local input API:** `http_parser.parser.HttpParser().execute(bytes, len(bytes))`
- **Documentation:** [API reference](<https://pypi.org/project/http-parser/0.9.0/>)
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
