# httppackets — HTTP/1.1 / Python

- **Pinned release:** `0.1.0a0`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 request head
- **Underlying family:** httppackets Lark grammar
- **Local input API:** `httppackets.http_1_1_parser.parse_http_1_1_requests(BytesIO(bytes), callbacks)`
- **Documentation:** [API reference](<https://pypi.org/project/httppackets/0.1.0a0/>)
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
