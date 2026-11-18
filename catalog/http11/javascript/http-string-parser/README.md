# http-string-parser — HTTP/1.1 / JavaScript

- **Pinned release:** `0.0.6`
- **Upstream:** [source repository](<https://github.com/apiaryio/http-string-parser>) · [npm](<https://www.npmjs.com/package/http-string-parser>)
- **License:** MIT
- **Parsed scope:** request
- **Underlying family:** http-string-parser
- **Local input API:** `parseRequest(rawString)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/http-string-parser>)
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

[Docker harness and verification receipt](../../../../projects/http11/javascript/http_string_parser/README.md)

```sh
python3 parsarium.py build http11 javascript http_string_parser
python3 parsarium.py run http11 javascript http_string_parser controls/http11/request.http
```
