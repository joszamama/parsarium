# parse-raw-http — HTTP/1.1 / JavaScript

- **Pinned release:** `0.0.1`
- **License:** MIT
- **Parsed scope:** response
- **Underlying family:** parse-raw-http
- **Local input API:** `parseResponse(Buffer,{decodeContentEncoding:true})`
- **Documentation:** [API reference](<https://www.npmjs.com/package/parse-raw-http>)
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

[Docker harness and verification receipt](../../../../projects/http11/javascript/parse_raw_http/README.md)

```sh
python3 parsarium.py build http11 javascript parse_raw_http
python3 parsarium.py run http11 javascript parse_raw_http controls/http11/request.http
```
