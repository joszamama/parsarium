# mina-http — HTTP/1.1 / Java

- **Pinned release:** `2.2.10`
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 request line and headers from local bytes
- **Underlying family:** Apache MINA native HTTP server decoder
- **Local input API:** `new HttpServerDecoder().decode(DummySession, IoBuffer.wrap(localBytes), ProtocolDecoderOutput); collect HttpRequest and read getMethod(), getRequestPath(), getQueryString(), getProtocolVersion(), getHeader(lowercaseName)`
- **Documentation:** [API reference](<https://nightlies.apache.org/mina/mina/2.2.10/apidocs/org/apache/mina/http/HttpServerDecoder.html>)
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

The 2.2.10 mina-http source writes a native HttpRequestImpl into ProtocolDecoderOutput; headers are normalized to lowercase. The Maven POM declares mina-core with bundle type, which Maven cannot resolve as a normal artifact; adapter POM excludes that broken transitive edge and explicitly pins the same mina-core JAR. slf4j-nop pins the 1.7 logger binding for deterministic quiet output.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
