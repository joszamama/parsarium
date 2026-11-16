# saf-httparser — HTTP/1.1 / Rust

- **Pinned release:** `0.1.1`
- **License:** MIT
- **Parsed scope:** request: method, URI, version
- **Underlying family:** saf-httparser
- **Local input API:** `request_from_bytes(&bytes)`
- **Documentation:** [API reference](<https://docs.rs/saf-httparser/0.1.1/saf_httparser/>)
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

[Docker harness and verification receipt](../../../../projects/http11/rust/saf_httparser/README.md)

```sh
python3 parsarium.py build http11 rust saf_httparser
python3 parsarium.py run http11 rust saf_httparser controls/http11/request.http
```
