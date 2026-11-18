# libhv — HTTP/1.1 / C++

- **Pinned release:** `1.3.1`
- **Upstream:** [source repository](<https://github.com/ithewei/libhv>)
- **License:** BSD-3-Clause AND MIT
- **Parsed scope:** HTTP/1.1 GET request method, target and version after complete header parse from local bytes
- **Underlying family:** libhv bundles a modified Node http-parser 2.9.1 C engine; separate tagged library distribution but shared parser family with Node http-parser 2.9.4, not an independent engine
- **Local input API:** `Bundled public C http_parser_init(HTTP_REQUEST), http_parser_execute(parser, callbacks, local request bytes, length), and http_method_str; on_url and on_headers_complete callbacks`
- **Documentation:** [API reference](<https://github.com/ithewei/libhv/blob/v1.3.1/http/http_parser.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/http11/parsers.json) · [control verification](../../../../data/cpp/http11/verification.json) · [within-ecosystem ranking](../../../../data/cpp/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "path": "/parsarium?x=1",
  "version": "1.1"
}
```

 Same release and underlying parser as C × HTTP/1.1; this C++ path is not an independent engine.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/cpp/libhv/README.md)

```sh
python3 parsarium.py build http11 cpp libhv
python3 parsarium.py run http11 cpp libhv controls/http11/request.http
```
