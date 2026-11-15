# workerman/psr7 — HTTP/1.1 / PHP

- **Pinned release:** `v2.0.2`
- **License:** MIT
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** Guzzle PSR-7 HTTP message parser
- **Local input API:** `Workerman\Psr7\parse_request(local raw HTTP/1.1 bytes); request line, target, version, headers`
- **Documentation:** [API reference](<https://github.com/walkor/psr7/blob/5f5b65e2462cd408f738cc967a80d8c15f9b57f3/README.md>)
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

Fork of older Guzzle PSR-7 code; shared parser lineage with ringcentral/psr7 and guzzlehttp/psr7.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
