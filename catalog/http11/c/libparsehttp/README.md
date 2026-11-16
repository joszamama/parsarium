# libparsehttp — HTTP/1.1 / C

- **Pinned release:** `0.06`
- **License:** GPL-2.0-or-later
- **Parsed scope:** HTTP/1.1 GET request method, path, query, version and Host from local byte buffer
- **Underlying family:** libparsehttp 0.06 standalone C HTTP request line/header scanner; separate implementation from Node http-parser and llhttp
- **Local input API:** `parse_init; parse_process(parsehttp_t *, local request bytes, length); registered callbacks report method, path, query, version, Host and completion`
- **Documentation:** [API reference](<https://github.com/clintwebb/libparsehttp/blob/v0.06/src/libparsehttp/parsehttp.h>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/c/libparsehttp/README.md)

```sh
python3 parsarium.py build http11 c libparsehttp
python3 parsarium.py run http11 c libparsehttp controls/http11/request.http
```
