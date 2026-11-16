# http-message-parser-ts — HTTP/1.1 / JavaScript

- **Pinned release:** `0.0.5`
- **License:** MIT
- **Parsed scope:** response
- **Underlying family:** http-message-parser-ts
- **Local input API:** `new HttpMessageParser().parseResponse(rawString)`
- **Documentation:** [API reference](<https://unpkg.com/http-message-parser-ts@0.0.5/dist/http-message-parser.d.ts>)
- **Catalog evidence:** [parser record](../../../../data/javascript/http11/parsers.json) · [control verification](../../../../data/javascript/http11/verification.json) · [within-ecosystem ranking](../../../../data/javascript/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "status": 200,
  "body": "parsarium"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/javascript/http_message_parser_ts/README.md)

```sh
python3 parsarium.py build http11 javascript http_message_parser_ts
python3 parsarium.py run http11 javascript http_message_parser_ts controls/http11/request.http
```
