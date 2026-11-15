# webparse — HTTP/1.1 / Rust

- **Pinned release:** `0.3.1`
- **License:** Apache-2.0
- **Parsed scope:** request: method, URL, consumed bytes
- **Underlying family:** webparse
- **Local input API:** `Request::<()>::parse(&bytes)`
- **Documentation:** [API reference](<https://docs.rs/webparse/0.3.1/webparse/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "consumed": 88,
  "method": "GET",
  "target": "http://example.test/parsarium?x=1"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
