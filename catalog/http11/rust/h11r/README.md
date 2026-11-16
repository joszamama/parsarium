# h11r — HTTP/1.1 / Rust

- **Pinned release:** `0.3.1`
- **License:** MIT
- **Parsed scope:** request event: method, target, version
- **Underlying family:** httparse core
- **Local input API:** `Connection::receive_data(&bytes); next_event()`
- **Documentation:** [API reference](<https://docs.rs/h11r/0.3.1/h11r/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "Method([71, 69, 84])",
  "target": "/parsarium?x=1",
  "version": "Http11"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/rust/h11r/README.md)

```sh
python3 parsarium.py build http11 rust h11r
python3 parsarium.py run http11 rust h11r controls/http11/request.http
```
