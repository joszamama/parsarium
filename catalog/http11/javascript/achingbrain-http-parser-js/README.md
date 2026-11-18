# @achingbrain/http-parser-js — HTTP/1.1 / JavaScript

- **Pinned release:** `0.5.9`
- **Upstream:** [source repository](<https://github.com/creationix/http-parser-js>) · [npm](<https://www.npmjs.com/package/@achingbrain/http-parser-js>)
- **License:** MIT
- **Parsed scope:** request
- **Underlying family:** http-parser-js
- **Local input API:** `new HTTPParser(REQUEST); onHeadersComplete callback; execute(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@achingbrain/http-parser-js>)
- **Catalog evidence:** [parser record](../../../../data/javascript/http11/parsers.json) · [control verification](../../../../data/javascript/http11/verification.json) · [within-ecosystem ranking](../../../../data/javascript/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1"
}
```

Fork of the creationix implementation.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/javascript/achingbrain_http_parser_js/README.md)

```sh
python3 parsarium.py build http11 javascript achingbrain_http_parser_js
python3 parsarium.py run http11 javascript achingbrain_http_parser_js controls/http11/request.http
```
