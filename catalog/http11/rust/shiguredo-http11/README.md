# shiguredo_http11 — HTTP/1.1 / Rust

- **Pinned release:** `2026.7.0-canary.2`
- **Upstream:** [source repository](<https://github.com/shiguredo/http11-rs>) · [crates.io](<https://crates.io/crates/shiguredo_http11>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/rust/shiguredo_http11/README.md)

```sh
python3 parsarium.py build http11 rust shiguredo_http11
python3 parsarium.py run http11 rust shiguredo_http11 controls/http11/request.http
```
