# http-muncher — HTTP/1.1 / Rust

- **Pinned release:** `0.3.2`
- **License:** MIT
- **Parsed scope:** streaming request: method, target, version, consumed bytes
- **Underlying family:** node/http-parser C binding
- **Local input API:** `Parser::request().parse(&mut ParserHandler, &bytes)`
- **Documentation:** [API reference](<https://docs.rs/http-muncher/0.3.2/http_muncher/>)
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

[Docker harness and verification receipt](../../../../projects/http11/rust/http_muncher/README.md)

```sh
python3 parsarium.py build http11 rust http_muncher
python3 parsarium.py run http11 rust http_muncher controls/http11/request.http
```
