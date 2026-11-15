# zenith-http1 — HTTP/1.1 / Rust

- **Pinned release:** `0.1.1`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** response: status, fields, body
- **Underlying family:** zenith-http1
- **Local input API:** `parse_response(&bytes)`
- **Documentation:** [API reference](<https://docs.rs/zenith-http1/0.1.1/zenith_http1/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/response.http`](../../../../controls/http11/response.http)

## Observed control result

```json
{
  "body": "parsarium",
  "headers": 2,
  "status": 200
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
