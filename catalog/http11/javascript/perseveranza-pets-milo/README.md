# @perseveranza-pets/milo — HTTP/1.1 / JavaScript

- **Pinned release:** `0.9.0`
- **License:** ISC
- **Parsed scope:** request
- **Underlying family:** milo
- **Local input API:** `setup(callbacks); create(); parse(parser,wasmPointer,length)`
- **Documentation:** [API reference](<https://github.com/ShogunPanda/milo/blob/main/docs/js.md>)
- **Catalog evidence:** [parser record](../../../../data/javascript/http11/parsers.json) · [control verification](../../../../data/javascript/http11/verification.json) · [within-ecosystem ranking](../../../../data/javascript/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1"
}
```

Rust parser compiled to WebAssembly.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
