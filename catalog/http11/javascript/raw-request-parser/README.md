# raw-request-parser — HTTP/1.1 / JavaScript

- **Pinned release:** `1.0.7`
- **License:** MIT
- **Parsed scope:** request
- **Underlying family:** raw-request-parser
- **Local input API:** `RawRequestParser.fromString(rawRequest)`
- **Documentation:** [API reference](<https://unpkg.com/raw-request-parser@1.0.7/lib/RawRequestParser.d.ts>)
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
