# httparse — HTTP/1.1 / Rust

- **Pinned release:** `1.10.1`
- **License:** MIT OR Apache-2.0
- **Parsed scope:** request head: method, target, HTTP minor version, headers
- **Underlying family:** httparse core
- **Local input API:** `Request::parse(&bytes) with header slots`
- **Documentation:** [API reference](<https://docs.rs/httparse/1.10.1/httparse/>)
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

[Docker harness and verification receipt](../../../../projects/http11/rust/httparse/README.md)

```sh
python3 parsarium.py build http11 rust httparse
python3 parsarium.py run http11 rust httparse controls/http11/request.http
```
