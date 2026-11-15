# llhttp — HTTP/1.1 / C

- **Pinned release:** `9.4.3`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 GET request method, target and version after complete header parse
- **Underlying family:** llhttp generated HTTP/1 parser, descended from Node http-parser design
- **Local input API:** `llhttp_init(..., HTTP_REQUEST, ...); llhttp_execute(llhttp_t *, local request bytes, length); on_url and on_headers_complete callbacks`
- **Documentation:** [API reference](<https://github.com/nodejs/llhttp#usage>)
- **Catalog evidence:** [parser record](../../../../data/c/http11/parsers.json) · [control verification](../../../../data/c/http11/verification.json) · [within-ecosystem ranking](../../../../data/c/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "path": "/parsarium?x=1",
  "version": "1.1"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
