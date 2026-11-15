# async-http-codec — HTTP/1.1 / Rust

- **Pinned release:** `0.8.0`
- **License:** Apache-2.0 OR MIT
- **Parsed scope:** async request head: method, URI, version, fields
- **Underlying family:** httparse core
- **Local input API:** `RequestHead::decode(futures::io::Cursor<Vec<u8>>)`
- **Documentation:** [API reference](<https://docs.rs/async-http-codec/0.8.0/async_http_codec/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "headers": 3,
  "method": "GET",
  "target": "/parsarium?x=1",
  "version": "HTTP/1.1"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
