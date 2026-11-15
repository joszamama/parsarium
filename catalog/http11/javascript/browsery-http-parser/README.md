# @browsery/http-parser — HTTP/1.1 / JavaScript

- **Pinned release:** `0.5.10-rev.1`
- **License:** MIT
- **Parsed scope:** request
- **Underlying family:** http-parser-js
- **Local input API:** `new HTTPParser(REQUEST); onHeadersComplete callback; execute(Buffer)`
- **Documentation:** [API reference](<https://www.npmjs.com/package/@browsery/http-parser>)
- **Catalog evidence:** [parser record](../../../../data/javascript/http11/parsers.json) · [control verification](../../../../data/javascript/http11/verification.json) · [within-ecosystem ranking](../../../../data/javascript/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1"
}
```

Browser-compatible fork of http-parser-js.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
