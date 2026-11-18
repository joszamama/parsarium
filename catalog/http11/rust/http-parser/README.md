# http_parser — HTTP/1.1 / Rust

- **Pinned release:** `0.0.2`
- **Upstream:** [source repository](<https://github.com/magic003/http-parser-rs>) · [crates.io](<https://crates.io/crates/http_parser>)
- **License:** MIT
- **Parsed scope:** streaming request: method, target, version, consumed bytes
- **Underlying family:** node/http-parser Rust port
- **Local input API:** `HttpParser::new(Request).execute(&mut HttpParserCallback, &bytes)`
- **Documentation:** [API reference](<https://docs.rs/http_parser/0.0.2/http_parser/>)
- **Catalog evidence:** [parser record](../../../../data/rust/http11/parsers.json) · [control verification](../../../../data/rust/http11/verification.json) · [within-ecosystem ranking](../../../../data/rust/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "consumed": 88,
  "method": "GET",
  "target": "/parsarium?x=1",
  "version": "1.1"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/rust/http_parser/README.md)

```sh
python3 parsarium.py build http11 rust http_parser
python3 parsarium.py run http11 rust http_parser controls/http11/request.http
```
