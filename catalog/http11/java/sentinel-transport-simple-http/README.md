# sentinel-transport-simple-http — HTTP/1.1 / Java

- **Pinned release:** `1.8.10`
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 response status line, status code, Content-Type header, and nine-byte body from local stream
- **Underlying family:** Sentinel native simple HTTP response parser
- **Local input API:** `new SimpleHttpResponseParser().parse(local InputStream); getStatusLine(), getStatusCode(), getHeader(name), getBodyAsString()`
- **Documentation:** [API reference](<https://github.com/alibaba/Sentinel/blob/1.8.10/sentinel-transport/sentinel-transport-simple-http/src/main/java/com/alibaba/csp/sentinel/transport/heartbeat/client/SimpleHttpResponseParser.java>)
- **Catalog evidence:** [parser record](../../../../data/java/http11/parsers.json) · [control verification](../../../../data/java/http11/verification.json) · [within-ecosystem ranking](../../../../data/java/http11/ranking.md)
- **Valid control:** [`controls/http11/response.http`](../../../../controls/http11/response.http)

## Observed control result

```json
{
  "status_line": "HTTP/1.1 200 OK",
  "status": 200,
  "content_type": "text/plain",
  "body": "parsarium"
}
```

Sentinel transport parses raw HTTP responses with Content-Length. Its documented parser does not support chunked responses; only the valid fixed-length control is verified. The adapter suppresses package startup log chatter while reporting parsed fields.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
