# angus/laminas-http — HTTP/1.1 / PHP

- **Pinned release:** `v1.0.4`
- **License:** BSD-3-Clause
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** Zend/Laminas HTTP message parser lineage
- **Local input API:** `Request::fromString(local raw HTTP/1.1 bytes); request line, target, version, headers`
- **Documentation:** [API reference](<https://github.com/angusaust/angus-laminas-http/blob/a5367dd33bc1321765d95d33b95faffb6c92f068/src/Request.php>)
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

Fork of Laminas HTTP request parser; same underlying lineage as laminas/laminas-http and zendframework/zend-http.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
