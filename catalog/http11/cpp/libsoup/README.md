# libsoup — HTTP/1.1 / C++

- **Pinned release:** `3.8.1`
- **License:** LGPL-2.0-or-later
- **Parsed scope:** HTTP/1.1 GET request-head method, target, version and Host header from local byte buffer
- **Underlying family:** GNOME libsoup 3 HTTP/1 request-head parser, independent from llhttp and PicoHTTPParser
- **Local input API:** `soup_headers_parse_request(local request-head bytes excluding trailing blank line, length, SoupMessageHeaders, method, path, version)`
- **Documentation:** [API reference](<https://libsoup.gnome.org/libsoup-3.0/func.headers_parse_request.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/http11/parsers.json) · [control verification](../../../../data/cpp/http11/verification.json) · [within-ecosystem ranking](../../../../data/cpp/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "path": "/parsarium?x=1",
  "version": "1.1",
  "host": "example.test"
}
```

 Same release and underlying parser as C × HTTP/1.1; this C++ path is not an independent engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
