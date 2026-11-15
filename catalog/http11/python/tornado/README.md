# tornado — HTTP/1.1 / Python

- **Pinned release:** `6.6.1`
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 response status, headers and body
- **Underlying family:** Tornado Python HTTP/1 parser
- **Local input API:** `tornado.http1connection.HTTP1Connection(local IOStream, is_client=True).read_response(delegate)`
- **Documentation:** [API reference](<https://www.tornadoweb.org/en/stable/http1connection.html>)
- **Catalog evidence:** [parser record](../../../../data/python/http11/parsers.json) · [control verification](../../../../data/python/http11/verification.json) · [within-ecosystem ranking](../../../../data/python/http11/ranking.md)
- **Valid control:** [`controls/http11/response.http`](../../../../controls/http11/response.http)

## Observed control result

```json
{
  "status": 200,
  "content_type": "text/plain",
  "body": "parsarium"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
