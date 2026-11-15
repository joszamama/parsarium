# workerman/workerman — HTTP/1.1 / PHP

- **Pinned release:** `v5.2.3`
- **License:** MIT
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** Workerman native HTTP request parser
- **Local input API:** `Protocols\Http\Request(local raw HTTP/1.1 bytes); method, target, version, headers`
- **Documentation:** [API reference](<https://github.com/walkor/workerman/blob/8fd5c148ff7dcd7bbc88621e1712eeb1f66b7f56/src/Protocols/Http/Request.php>)
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

Direct public request constructor and accessors in the pinned Workerman server package; separate from workerman/psr7.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
