# request-http-parser — HTTP/1.1 / Rust

- **Pinned release:** `0.1.4`
- **License:** MIT
- **Parsed scope:** request: method, path, query, headers; does not expose HTTP version
- **Underlying family:** request-http-parser
- **Local input API:** `parser::Request::new(request_str)`
- **Documentation:** [API reference](<https://docs.rs/request-http-parser/0.1.4/request_http_parser/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "host": "example.test",
  "method": "GET",
  "path": "/parsarium",
  "query_x": "1"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/rust/request_http_parser/README.md)

```sh
python3 parsarium.py build http11 rust request_http_parser
python3 parsarium.py run http11 rust request_http_parser controls/http11/request.http
```
