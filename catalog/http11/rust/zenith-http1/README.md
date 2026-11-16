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

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/rust/zenith_http1/README.md)

```sh
python3 parsarium.py build http11 rust zenith_http1
python3 parsarium.py run http11 rust zenith_http1 controls/http11/response.http
```
