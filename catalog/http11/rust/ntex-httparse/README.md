# ntex-httparse — HTTP/1.1 / Rust

- **Pinned release:** `2.4.0`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** request line: method, target, HTTP minor version
- **Underlying family:** ntex-httparse fork
- **Local input API:** `Request::parse(&bytes)`
- **Documentation:** [API reference](<https://docs.rs/ntex-httparse/2.4.0/ntex_httparse/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "minor": 1,
  "target": "/parsarium?x=1"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/rust/ntex_httparse/README.md)

```sh
python3 parsarium.py build http11 rust ntex_httparse
python3 parsarium.py run http11 rust ntex_httparse controls/http11/request.http
```
