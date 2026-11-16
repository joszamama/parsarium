# weida-http-codec — HTTP/1.1 / Rust

- **Pinned release:** `0.1.0-alpha.14`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** request head: method, target, version, fields
- **Underlying family:** weida-http-codec
- **Local input API:** `h1::decode_request(&bytes, Limits::default())`
- **Documentation:** [API reference](<https://docs.rs/weida-http-codec/0.1.0-alpha.14/weida_http_codec/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "headers": 3,
  "method": "GET",
  "minor": 1,
  "target": "/parsarium?x=1"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/rust/weida_http_codec/README.md)

```sh
python3 parsarium.py build http11 rust weida_http_codec
python3 parsarium.py run http11 rust weida_http_codec controls/http11/request.http
```
