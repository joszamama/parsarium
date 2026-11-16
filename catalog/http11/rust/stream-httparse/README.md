# stream-httparse — HTTP/1.1 / Rust

- **Pinned release:** `0.2.6`
- **License:** MIT
- **Parsed scope:** streaming request: method, target, protocol
- **Underlying family:** stream-httparse
- **Local input API:** `ReqParser::block_parse(&bytes); finish()`
- **Documentation:** [API reference](<https://docs.rs/stream-httparse/0.2.6/stream_httparse/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "protocol": "HTTP/1.1",
  "target": "/parsarium?x=1"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/rust/stream_httparse/README.md)

```sh
python3 parsarium.py build http11 rust stream_httparse
python3 parsarium.py run http11 rust stream_httparse controls/http11/request.http
```
