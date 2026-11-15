# jwat-common — HTTP/1.1 / Java

- **Pinned release:** `1.2.1`
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 request line and headers from local stream
- **Underlying family:** JWAT native HTTP header parser
- **Local input API:** `org.jwat.common.HttpHeader.processPayload(HT_REQUEST, local ByteCountingPushBackInputStream, length, null); method, requestUri, httpVersion, getHeader(name)`
- **Documentation:** [API reference](<https://github.com/netarchivesuite/jwat/blob/jwat-1.2.1/jwat-common/src/main/java/org/jwat/common/HttpHeader.java>)
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

WARC toolkit jwat-common exposes HttpHeader.processPayload for both request and response messages; the adapter feeds a local stream and checks isValid(). No WARC container is needed.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
