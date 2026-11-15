# webarchive-commons — HTTP/1.1 / Java

- **Pinned release:** `3.0.5`
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 request line and headers from local stream
- **Underlying family:** webarchive-commons native HTTP message parser
- **Local input API:** `new org.archive.format.http.HttpRequestParser().parse(local InputStream); getMessage(), getHeaders()`
- **Documentation:** [API reference](<https://github.com/iipc/webarchive-commons/blob/webarchive-commons-3.0.5/src/main/java/org/archive/format/http/HttpRequestParser.java>)
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

WARC utility library exposes a direct HttpRequestParser that composes its own request-line and header parsers. No WARC container is needed for this control.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
