# httpcore-nio — HTTP/1.1 / Java

- **Pinned release:** `4.4.16`
- **Upstream:** [Maven Central](<https://central.sonatype.com/artifact/org.apache.httpcomponents/httpcore-nio>)
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 request line and headers from local channel
- **Underlying family:** Apache HttpComponents Core 4.x NIO request parser
- **Local input API:** `new DefaultHttpRequestParser(SessionInputBufferImpl); fillBuffer(local ReadableByteChannel); parse() as HttpRequest`
- **Documentation:** [API reference](<https://hc.apache.org/httpcomponents-core-4.4.x/current/httpcore-nio/apidocs/org/apache/http/nio/NHttpMessageParser.html>)
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

Separate Maven artifact and NIO parser class from blocking httpcore 4.4.16, but same Apache HttpComponents project and shared line parser ancestry. The documented NIO API parses the message head, not an entity body.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/java/httpcore_nio/README.md)

```sh
python3 parsarium.py build http11 java httpcore_nio
python3 parsarium.py run http11 java httpcore_nio controls/http11/request.http
```
