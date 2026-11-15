# http-headers — HTTP/1.1 / JavaScript

- **Pinned release:** `3.0.2`
- **License:** MIT
- **Parsed scope:** request
- **Underlying family:** http-headers
- **Local input API:** `httpHeaders(rawBuffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/http-headers>)
- **Catalog evidence:** [parser record](../../../../data/javascript/http11/parsers.json) · [control verification](../../../../data/javascript/http11/verification.json) · [within-ecosystem ranking](../../../../data/javascript/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1"
}
```

Parses start line and header block; body parsing is outside its documented scope.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
