# libwebsockets — HTTP/1.1 / C++

- **Pinned release:** `5.0.0`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 GET request method, path, query argument and Host header from local read buffer
- **Underlying family:** libwebsockets C HTTP/1 parser in the server adoption path; independent from llhttp and LibHTP
- **Local input API:** `lws_create_context in no-listen server mode; lws_adopt_socket_vhost_readbuf(vhost, local socketpair fd, local HTTP request bytes, length); LWS_CALLBACK_HTTP and parsed header/query accessors`
- **Documentation:** [API reference](<https://github.com/warmcat/libwebsockets/blob/v5.0.0/include/libwebsockets/lws-adopt.h>)
- **Catalog evidence:** [parser record](../../../../data/cpp/http11/parsers.json) · [control verification](../../../../data/cpp/http11/verification.json) · [within-ecosystem ranking](../../../../data/cpp/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "path": "/parsarium?x=1",
  "host": "example.test"
}
```

 Same release and underlying parser as C × HTTP/1.1; this C++ path is not an independent engine.

The Docker harness accepts at most 2048 initial bytes, the documented limit of lws_adopt_socket_vhost_readbuf; larger inputs are rejected before parsing.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/cpp/libwebsockets/README.md)

```sh
python3 parsarium.py build http11 cpp libwebsockets
python3 parsarium.py run http11 cpp libwebsockets controls/http11/request.http
```
