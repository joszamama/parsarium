# finwo-http-parser — HTTP/1.1 / C++

- **Pinned release:** `stable@3d78ef3ad068`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 GET request method, path, query, version and Host from local byte buffer
- **Underlying family:** finwo/http-parser.c independent C request/header/body parser; not the Node http-parser family despite similar name
- **Local input API:** `http_parser_request_init; http_parser_request_data(request, local struct buf of saved bytes); request ready flag, method/path/query/version fields and http_parser_header_get`
- **Documentation:** [API reference](<https://github.com/finwo/http-parser.c/blob/3d78ef3ad068696b0d3f5b9bc672771a89805a5f/README.md>)
- **Catalog evidence:** [parser record](../../../../data/cpp/http11/parsers.json) · [control verification](../../../../data/cpp/http11/verification.json) · [within-ecosystem ranking](../../../../data/cpp/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "path": "/parsarium",
  "query": "x=1",
  "version": "1.1",
  "host": "example.test"
}
```

 Same release and underlying parser as C × HTTP/1.1; this C++ path is not an independent engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/cpp/finwo-http-parser/README.md)

```sh
python3 parsarium.py build http11 cpp finwo-http-parser
python3 parsarium.py run http11 cpp finwo-http-parser controls/http11/request.http
```
