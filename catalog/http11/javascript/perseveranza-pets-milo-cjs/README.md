# @perseveranza-pets/milo-cjs — HTTP/1.1 / JavaScript

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

CommonJS distribution of the same Rust/WebAssembly parser.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/javascript/perseveranza_pets_milo_cjs/README.md)

```sh
python3 parsarium.py build http11 javascript perseveranza_pets_milo_cjs
python3 parsarium.py run http11 javascript perseveranza_pets_milo_cjs controls/http11/request.http
```
