# http-parser-ts — HTTP/1.1 / JavaScript

- **Pinned release:** `0.1.3`
- **License:** MIT
- **Parsed scope:** request
- **Underlying family:** http-parser-ts
- **Local input API:** `new HTTPParser(); initialize(REQUEST); callbacks; execute(Buffer)`
- **Documentation:** [API reference](<https://unpkg.com/http-parser-ts@0.1.3/build/index.d.ts>)
- **Catalog evidence:** [parser record](../../../../data/javascript/http11/parsers.json) · [control verification](../../../../data/javascript/http11/verification.json) · [within-ecosystem ranking](../../../../data/javascript/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1"
}
```

Separate TypeScript rewrite based on the http-parser-js design.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/javascript/http_parser_ts/README.md)

```sh
python3 parsarium.py build http11 javascript http_parser_ts
python3 parsarium.py run http11 javascript http_parser_ts controls/http11/request.http
```
