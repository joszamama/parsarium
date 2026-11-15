# httpcore5 — HTTP/1.1 / Java

- **Pinned release:** `5.4.4`
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 request line and headers from local stream
- **Underlying family:** Apache HttpComponents Core HTTP/1.1 parser, 5.x branch
- **Local input API:** `new DefaultHttpRequestParser().parse(SessionInputBufferImpl, InputStream)`
- **Documentation:** [API reference](<https://hc.apache.org/httpcomponents-core-5.4.x/5.4.4/httpcore5/apidocs/org/apache/hc/core5/http/impl/io/DefaultHttpRequestParser.html>)
- **Catalog evidence:** [parser record](../../../../data/java/http11/parsers.json) · [control verification](../../../../data/java/http11/verification.json) · [within-ecosystem ranking](../../../../data/java/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "version": "HTTP/1.1",
  "host": "example.test",
  "x_parsarium": "yes"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
