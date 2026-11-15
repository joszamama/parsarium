# h11pro — HTTP/1.1 / Python

- **Pinned release:** `0.0.1`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 request head
- **Underlying family:** h11 code fork
- **Local input API:** `h11pro.Connection(h11pro.SERVER).receive_data(bytes); next_event()`
- **Documentation:** [API reference](<https://pypi.org/project/h11pro/0.0.1/>)
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
