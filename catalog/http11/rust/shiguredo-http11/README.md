# shiguredo_http11 — HTTP/1.1 / Rust

- **Pinned release:** `2026.7.0-canary.2`
- **License:** Apache-2.0
- **Parsed scope:** request head: method, URI, version
- **Underlying family:** shiguredo_http11
- **Local input API:** `RequestDecoder::feed(&bytes); decode()`
- **Documentation:** [API reference](<https://docs.rs/shiguredo_http11/2026.7.0-canary.2/shiguredo_http11/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "version": "HTTP/1.1"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
