# async-h1 — HTTP/1.1 / Rust

- **Pinned release:** `2.3.4`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** async response: status, body
- **Underlying family:** httparse core
- **Local input API:** `client::decode(futures_lite::io::Cursor<Vec<u8>>)`
- **Documentation:** [API reference](<https://docs.rs/async-h1/2.3.4/async_h1/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/response.http`](../../../../controls/http11/response.http)

## Observed control result

```json
{
  "body": "parsarium",
  "status": 200
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/rust/async_h1/README.md)

```sh
python3 parsarium.py build http11 rust async_h1
python3 parsarium.py run http11 rust async_h1 controls/http11/response.http
```
