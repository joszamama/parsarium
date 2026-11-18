# http-message-parser — HTTP/1.1 / JavaScript

- **Pinned release:** `0.0.34`
- **Upstream:** [source repository](<https://github.com/miguelmota/http-message-parser>) · [npm](<https://www.npmjs.com/package/http-message-parser>)
- **License:** MIT
- **Parsed scope:** request
- **Underlying family:** http-message-parser
- **Local input API:** `parse(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/http-message-parser>)
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

[Docker harness and verification receipt](../../../../projects/http11/javascript/http_message_parser/README.md)

```sh
python3 parsarium.py build http11 javascript http_message_parser
python3 parsarium.py run http11 javascript http_message_parser controls/http11/request.http
```
