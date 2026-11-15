# jetty-http — HTTP/1.1 / Java

- **Pinned release:** `12.1.15`
- **License:** EPL-2.0 OR Apache-2.0
- **Parsed scope:** HTTP/1.1 request line and headers from local bytes
- **Underlying family:** Jetty HTTP/1.1 HttpParser
- **Local input API:** `HttpTester.parseRequest(ByteBuffer.wrap(localBytes)) returns Request; backed by HttpParser.parseNext(ByteBuffer)`
- **Documentation:** [API reference](<https://javadoc.jetty.org/jetty-12.1/org/eclipse/jetty/http/HttpTester.html>)
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
