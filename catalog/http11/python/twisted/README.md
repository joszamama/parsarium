# Twisted — HTTP/1.1 / Python

- **Pinned release:** `26.10.0`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 request head
- **Underlying family:** Twisted HTTPChannel parser
- **Local input API:** `twisted.web.http.HTTPChannel.dataReceived(local HTTP bytes) with Request.process callback`
- **Documentation:** [API reference](<https://docs.twisted.org/en/latest/api/twisted.web.http.HTTPChannel.html>)
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
