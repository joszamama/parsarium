# phly/http — HTTP/1.1 / PHP

- **Pinned release:** `0.14.1`
- **License:** BSD-2-Clause
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** Diactoros HTTP message parser lineage
- **Local input API:** `Request\Serializer::fromString(local raw HTTP/1.1 bytes); request line, target, version, headers`
- **Documentation:** [API reference](<https://github.com/phly/http/blob/0d02d98106caf418a6b4031f2bf5fce3293faddc/README.md>)
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

Older Phly serializer; same project lineage later continued through Zend and Laminas Diactoros.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
