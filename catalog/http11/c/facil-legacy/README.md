# facil-legacy — HTTP/1.1 / C

- **Pinned release:** `0.7.6`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 GET request method, path, query, version and Host header after complete local-byte parse
- **Underlying family:** facil.io 0.7 HTTP/1 parser, earlier distinct distribution and API of the facil.io family later developed as C STL 0.8; these two package paths share lineage
- **Local input API:** `http1_parse(http1_parser_s *, local writable request bytes, length); method, path, query, version, header and request-complete callbacks`
- **Documentation:** [API reference](<https://github.com/boazsegev/facil.io/blob/0.7.6/lib/facil/http/parsers/http1_parser.h>)
- **Catalog evidence:** [parser record](../../../../data/c/http11/parsers.json) · [control verification](../../../../data/c/http11/verification.json) · [within-ecosystem ranking](../../../../data/c/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "path": "/parsarium",
  "query": "x=1",
  "version": "HTTP/1.1",
  "host": "example.test"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
