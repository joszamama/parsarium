# minihttpse — HTTP/1.1 / Rust

- **Pinned release:** `0.1.6`
- **License:** MIT/Apache-2.0
- **Parsed scope:** response: status, reason, body
- **Underlying family:** minihttpse
- **Local input API:** `Response::new(bytes.to_vec())`
- **Documentation:** [API reference](<https://docs.rs/minihttpse/0.1.6/minihttpse/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/response.http`](../../../../controls/http11/response.http)

## Observed control result

```json
{
  "body": "parsarium",
  "reason": "OK",
  "status": 200
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
