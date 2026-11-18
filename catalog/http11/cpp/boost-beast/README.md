# boost_beast — HTTP/1.1 / C++

- **Pinned release:** `1.92.0`
- **Upstream:** [source repository](<https://github.com/boostorg/beast>)
- **License:** BSL-1.0
- **Parsed scope:** HTTP/1.1 request method, target, version, and Host header
- **Underlying family:** Boost.Beast native HTTP parser
- **Local input API:** `boost::beast::http::request_parser<empty_body>::put(boost::asio::buffer(local_bytes), error_code&)`
- **Documentation:** [API reference](<https://www.boost.org/latest/libs/beast/doc/html/beast/ref/boost__beast__http__basic_parser/put.html>)
- **Catalog evidence:** [parser record](../../../../data/cpp/http11/parsers.json) · [control verification](../../../../data/cpp/http11/verification.json) · [within-ecosystem ranking](../../../../data/cpp/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "path": "/parsarium?x=1",
  "version": "1.1",
  "host": "example.test"
}
```

Native C++ parser; uses Boost.Asio buffers but does not delegate to a C HTTP parser.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/cpp/boost_beast/README.md)

```sh
python3 parsarium.py build http11 cpp boost_beast
python3 parsarium.py run http11 cpp boost_beast controls/http11/request.http
```
