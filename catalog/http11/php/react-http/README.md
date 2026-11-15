# react/http — HTTP/1.1 / PHP

- **Pinned release:** `v1.12.0`
- **License:** MIT
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** ReactPHP native HTTP server parser
- **Local input API:** `HttpServer::listen(local loopback socket); request handler receives parsed HTTP/1.1 method, target, version, headers`
- **Documentation:** [API reference](<https://github.com/reactphp/http/blob/37f13159cdcaf2b1387020751aa1ae1882477f78/README.md>)
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

Pinned ReactPHP HTTP server parses the saved raw request over a local TCP byte stream.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
