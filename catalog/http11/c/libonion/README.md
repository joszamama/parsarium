# libonion — HTTP/1.1 / C

- **Pinned release:** `0.8`
- **License:** Apache-2.0
- **Parsed scope:** HTTP/1.1 GET request method, path, query value, version and Host header from local byte buffer
- **Underlying family:** libonion C HTTP/1 request state machine in request_parser.c, independent from llhttp and PicoHTTPParser
- **Local input API:** `onion_request_new(NULL); onion_request_write(request, local request bytes, length); onion_request_get_fullpath/get_query/get_header/get_flags access parsed fields`
- **Documentation:** [API reference](<https://github.com/davidmoreno/onion/blob/v0.8/src/onion/request.h>)
- **Catalog evidence:** [parser record](../../../../data/c/http11/parsers.json) · [control verification](../../../../data/c/http11/verification.json) · [within-ecosystem ranking](../../../../data/c/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "path": "/parsarium",
  "version": "1.1",
  "host": "example.test",
  "query_x": "1"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
