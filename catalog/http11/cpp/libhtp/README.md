# libhtp — HTTP/1.1 / C++

- **Pinned release:** `0.5.53`
- **License:** BSD-3-Clause
- **Parsed scope:** HTTP/1.1 GET request method, target, version and parsed header table from local byte buffer
- **Underlying family:** OISF LibHTP independent C HTTP request/response stream parser
- **Local input API:** `htp_config_create; htp_connp_create/open; htp_connp_req_data(parser, timestamp, local request bytes, length); transaction request_method, request_uri, request_protocol and headers`
- **Documentation:** [API reference](<https://github.com/OISF/libhtp/blob/0.5.53/docs/QUICK_START>)
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
