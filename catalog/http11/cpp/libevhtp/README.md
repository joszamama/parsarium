# libevhtp — HTTP/1.1 / C++

- **Pinned release:** `1.2.9`
- **License:** BSD-3-Clause
- **Parsed scope:** HTTP/1.1 GET request method, path, query and version after complete headers
- **Underlying family:** libevhtp bundled htparse C HTTP/1 request scanner; source distributed and header installed by libevhtp
- **Local input API:** `htparser_new; htparser_init(..., htp_type_request); htparser_run(parser, hooks, local request bytes, length); path and args callbacks plus method/version accessors`
- **Documentation:** [API reference](<https://github.com/ellzey/libevhtp/blob/1.2.9/htparse/htparse.h>)
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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
