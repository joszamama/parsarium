# grizzly-http — HTTP/1.1 / Java

- **Pinned release:** `5.0.3`
- **Upstream:** [source repository](<https://github.com/eclipse-ee4j/glassfish-grizzly>) · [Maven Central](<https://central.sonatype.com/artifact/org.glassfish.grizzly/grizzly-http>)
- **License:** EPL-2.0 OR GPL-2.0 WITH Classpath-exception-2.0
- **Parsed scope:** HTTP/1.1 request line and headers from local bytes
- **Underlying family:** Grizzly native HTTP server codec
- **Local input API:** `HttpServerFilter.handleRead(FilterChainContext containing Buffers.wrap(MemoryManager, localBytes)); context.getMessage() as HttpContent; getHttpHeader() as HttpRequestPacket`
- **Documentation:** [API reference](<https://github.com/eclipse-ee4j/glassfish-grizzly/blob/5.0.3/modules/http/src/main/java/org/glassfish/grizzly/http/HttpServerFilter.java>)
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

The pinned Grizzly HttpServerFilter decodes an in-memory Buffer into HttpContent carrying its native HttpRequestPacket. The adapter constructs an unconnected TCPNIOConnection solely as a filter context; no listener or network request is involved. The handler returns method, target, protocol and headers.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/java/grizzly_http/README.md)

```sh
python3 parsarium.py build http11 java grizzly_http
python3 parsarium.py run http11 java grizzly_http controls/http11/request.http
```
