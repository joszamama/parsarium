# xocomil — HTTP/1.1 / Rust

- **Pinned release:** `0.3.0`
- **License:** MIT
- **Parsed scope:** request head: method, target, version
- **Underlying family:** xocomil
- **Local input API:** `request::Request::<16>::parse(&bytes)`
- **Documentation:** [API reference](<https://docs.rs/xocomil/0.3.0/xocomil/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "Get",
  "target": "/parsarium?x=1",
  "version": "Http11"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
