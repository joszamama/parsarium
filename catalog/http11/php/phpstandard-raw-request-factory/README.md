# phpstandard/raw-request-factory — HTTP/1.1 / PHP

- **Pinned release:** `1.0.1`
- **License:** MIT
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** PHPStandard raw HTTP request parser
- **Local input API:** `RawRequestFactory::createServerRequest(local raw HTTP/1.1 bytes); request line, target, version, headers`
- **Documentation:** [API reference](<https://github.com/phpstandard/raw-request-factory/blob/828a7a896376c7451317bb53dd2774446dd8ed63/README.md>)
- **Catalog evidence:** [parser record](../../../../data/php/http11/parsers.json) · [control verification](../../../../data/php/http11/verification.json) · [within-ecosystem ranking](../../../../data/php/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "target": "/parsarium?x=1",
  "version": "1.1",
  "host": "example.test",
  "custom": "yes"
}
```

Native raw-message parser creates a PSR-7 server request using pinned Guzzle PSR-7 2.13.1 factories.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
