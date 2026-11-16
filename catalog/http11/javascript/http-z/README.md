# http-z — HTTP/1.1 / JavaScript

- **Pinned release:** `8.1.1`
- **License:** MIT
- **Parsed scope:** request
- **Underlying family:** http-z
- **Local input API:** `parse(rawMessage:string)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/http-z>)
- **Catalog evidence:** [parser record](../../../../data/javascript/http11/parsers.json) · [control verification](../../../../data/javascript/http11/verification.json) · [within-ecosystem ranking](../../../../data/javascript/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1"
}
```

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
