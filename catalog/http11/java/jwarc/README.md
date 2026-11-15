# jwarc — HTTP/1.1 / Java

- **Pinned release:** `0.37.0`
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 request line and headers from local channel
- **Underlying family:** jwarc native HTTP parser
- **Local input API:** `org.netpreserve.jwarc.HttpRequest.parse(local ReadableByteChannel); method(), target(), version(), headers().first(name)`
- **Documentation:** [API reference](<https://github.com/iipc/jwarc/blob/v0.37.0/src/org/netpreserve/jwarc/HttpRequest.java>)
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

WARC library exposes its own direct HttpRequest.parse(ReadableByteChannel) API; no WARC container is needed for this control.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
