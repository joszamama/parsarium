# h11r — HTTP/1.1 / Rust

- **Pinned release:** `0.3.1`
- **License:** MIT
- **Parsed scope:** request event: method, target, version
- **Underlying family:** httparse core
- **Local input API:** `Connection::receive_data(&bytes); next_event()`
- **Documentation:** [API reference](<https://docs.rs/h11r/0.3.1/h11r/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "Method([71, 69, 84])",
  "target": "/parsarium?x=1",
  "version": "Http11"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
