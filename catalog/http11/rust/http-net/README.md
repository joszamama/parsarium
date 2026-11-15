# http-net — HTTP/1.1 / Rust

- **Pinned release:** `0.9.2`
- **License:** Apache-2.0 OR MIT
- **Parsed scope:** request head: method, target, version
- **Underlying family:** http-net
- **Local input API:** `parse_request_head(&bytes, &Limits, &mut fields)`
- **Documentation:** [API reference](<https://docs.rs/http-net/0.9.2/http_net/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "version": "Http11"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
