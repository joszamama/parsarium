# raw-http-parser — HTTP/1.1 / JavaScript

- **Pinned release:** `1.3.9`
- **License:** ISC
- **Parsed scope:** request
- **Underlying family:** raw-http-parser
- **Local input API:** `new HTTPRequest(Buffer)`
- **Documentation:** [API reference](<https://unpkg.com/raw-http-parser@1.3.9/types/index.d.ts>)
- **Catalog evidence:** [parser record](../../../../data/javascript/http11/parsers.json) · [control verification](../../../../data/javascript/http11/verification.json) · [within-ecosystem ranking](../../../../data/javascript/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/javascript/raw_http_parser/README.md)

```sh
python3 parsarium.py build http11 javascript raw_http_parser
python3 parsarium.py run http11 javascript raw_http_parser controls/http11/request.http
```
