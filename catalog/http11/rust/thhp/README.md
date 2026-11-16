# thhp — HTTP/1.1 / Rust

- **Pinned release:** `0.2.0`
- **License:** MIT
- **Parsed scope:** request head: method, target, HTTP minor version, fields
- **Underlying family:** thhp
- **Local input API:** `Request::parse(&bytes, &mut header_fields)`
- **Documentation:** [API reference](<https://docs.rs/thhp/0.2.0/thhp/>)
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

[Docker harness and verification receipt](../../../../projects/http11/rust/thhp/README.md)

```sh
python3 parsarium.py build http11 rust thhp
python3 parsarium.py run http11 rust thhp controls/http11/request.http
```
