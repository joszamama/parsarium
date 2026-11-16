# parse-http-header-line — HTTP/1.1 / Python

- **Pinned release:** `0.1.0`
- **License:** MIT
- **Parsed scope:** HTTP Host header field line only
- **Underlying family:** parse-http-header-line Python parser
- **Local input API:** `parse_http_header_line.parse_name_value(local request Host field line)`
- **Documentation:** [API reference](<https://pypi.org/project/parse-http-header-line/0.1.0/>)
- **Catalog evidence:** [parser record](../../../../data/python/http11/parsers.json) · [control verification](../../../../data/python/http11/verification.json) · [within-ecosystem ranking](../../../../data/python/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "header": "host",
  "value": "example.test"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
