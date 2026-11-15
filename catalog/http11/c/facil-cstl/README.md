# facil-cstl — HTTP/1.1 / C

- **Pinned release:** `0.8.5`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 GET request method, target, version and Host header after complete local-byte parse
- **Underlying family:** facil.io C STL 0.8 HTTP/1.x parser in 004 http1 parser.h; successor family to the separate facil.io 0.7 distribution and API, independent from llhttp and PicoHTTPParser
- **Local input API:** `fio_http1_parse(fio_http1_parser_s *, local writable request bytes as fio_buf_info_s, callback state); method, URL, version, header and completion callbacks`
- **Documentation:** [API reference](<https://github.com/facil-io/cstl/blob/0.8.5/fio-stl/004%20http1%20parser.md>)
- **Catalog evidence:** [parser record](../../../../data/c/http11/parsers.json) · [control verification](../../../../data/c/http11/verification.json) · [within-ecosystem ranking](../../../../data/c/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "path": "/parsarium?x=1",
  "version": "HTTP/1.1",
  "host": "example.test"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
