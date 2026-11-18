# http-kit-h1 — HTTP/1.1 / Rust

- **Pinned release:** `0.6.2`
- **Upstream:** [source repository](<https://github.com/zen-rs/http-kit>) · [crates.io](<https://crates.io/crates/http-kit-h1>)
- **License:** MIT
- **Parsed scope:** request head: method, URI, connection semantics
- **Underlying family:** httparse core
- **Local input API:** `proto::parse_request_head(&mut BytesMut, &Limits)`
- **Documentation:** [API reference](<https://docs.rs/http-kit-h1/0.6.2/http_kit_h1/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "keep_alive": false,
  "method": "GET",
  "target": "/parsarium?x=1"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/rust/http_kit_h1/README.md)

```sh
python3 parsarium.py build http11 rust http_kit_h1
python3 parsarium.py run http11 rust http_kit_h1 controls/http11/request.http
```
