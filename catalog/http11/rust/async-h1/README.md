# async-h1 — HTTP/1.1 / Rust

- **Pinned release:** `2.3.4`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** async response: status, body
- **Underlying family:** httparse core
- **Local input API:** `client::decode(futures_lite::io::Cursor<Vec<u8>>)`
- **Documentation:** [API reference](<https://docs.rs/async-h1/2.3.4/async_h1/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/response.http`](../../../../controls/http11/response.http)

## Observed control result

```json
{
  "body": "parsarium",
  "status": 200
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
