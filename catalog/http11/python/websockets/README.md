# websockets — HTTP/1.1 / Python

- **Pinned release:** `17.3`
- **License:** BSD-3-Clause
- **Parsed scope:** HTTP/1.1 handshake request head
- **Underlying family:** websockets Python HTTP/1.1 parser
- **Local input API:** `websockets.http11.Request.parse(read_line from local bytes)`
- **Documentation:** [API reference](<https://websockets.readthedocs.io/en/stable/reference/datastructures.html>)
- **Catalog evidence:** [parser record](../../../../data/python/http11/parsers.json) · [control verification](../../../../data/python/http11/verification.json) · [within-ecosystem ranking](../../../../data/python/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "target": "/parsarium?x=1",
  "host": "example.test"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
