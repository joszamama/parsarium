# @perseveranza-pets/milo — HTTP/1.1 / JavaScript

- **Pinned release:** `0.9.0`
- **Upstream:** [source repository](<https://github.com/ShogunPanda/milo>) · [npm](<https://www.npmjs.com/package/@perseveranza-pets/milo>)
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

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/javascript/perseveranza_pets_milo/README.md)

```sh
python3 parsarium.py build http11 javascript perseveranza_pets_milo
python3 parsarium.py run http11 javascript perseveranza_pets_milo controls/http11/request.http
```
