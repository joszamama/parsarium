# libparsehttp — HTTP/1.1 / C++

- **Pinned release:** `0.06`
- **License:** GPL-2.0-or-later
- **Parsed scope:** HTTP/1.1 GET request method, path, query, version and Host from local byte buffer
- **Underlying family:** libparsehttp 0.06 standalone C HTTP request line/header scanner; separate implementation from Node http-parser and llhttp
- **Local input API:** `parse_init; parse_process(parsehttp_t *, local request bytes, length); registered callbacks report method, path, query, version, Host and completion`
- **Documentation:** [API reference](<https://github.com/clintwebb/libparsehttp/blob/v0.06/src/libparsehttp/parsehttp.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/http11/parsers.json) · [control verification](../../../../data/cpp/http11/verification.json) · [within-ecosystem ranking](../../../../data/cpp/http11/ranking.md)
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

 Same release and underlying parser as C × HTTP/1.1; this C++ path is not an independent engine.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
