# blazingly-wire — HTTP/1.1 / Rust

- **Pinned release:** `0.1.3`
- **License:** MIT
- **Parsed scope:** request head: method, target, connection semantics
- **Underlying family:** httparse core
- **Local input API:** `parse_request_head(&bytes, Limits::default())`
- **Documentation:** [API reference](<https://docs.rs/blazingly-wire/0.1.3/blazingly_wire/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "keep_alive": false,
  "method": "Get",
  "target": "/parsarium?x=1"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/rust/blazingly_wire/README.md)

```sh
python3 parsarium.py build http11 rust blazingly_wire
python3 parsarium.py run http11 rust blazingly_wire controls/http11/request.http
```
