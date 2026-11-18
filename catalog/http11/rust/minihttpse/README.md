# minihttpse — HTTP/1.1 / Rust

- **Pinned release:** `0.1.6`
- **Upstream:** [crates.io](<https://crates.io/crates/minihttpse>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/rust/minihttpse/README.md)

```sh
python3 parsarium.py build http11 rust minihttpse
python3 parsarium.py run http11 rust minihttpse controls/http11/response.http
```
