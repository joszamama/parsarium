# @browsercore/http1 — HTTP/1.1 / JavaScript

- **Pinned release:** `0.2.2`
- **License:** MIT
- **Parsed scope:** response
- **Underlying family:** browsercore/http1
- **Local input API:** `parseResponse(Uint8Array)`
- **Documentation:** [API reference](<https://github.com/jverneuer/browsercore-http1>)
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

[Docker harness and verification receipt](../../../../projects/http11/javascript/browsercore_http1/README.md)

```sh
python3 parsarium.py build http11 javascript browsercore_http1
python3 parsarium.py run http11 javascript browsercore_http1 controls/http11/request.http
```
