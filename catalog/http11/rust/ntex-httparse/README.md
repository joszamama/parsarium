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

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
