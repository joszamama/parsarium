# alexpts/http-message-parser — HTTP/1.1 / PHP

- **Pinned release:** `0.0.3`
- **License:** MIT
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** AlexPTS HTTP message parser
- **Local input API:** `Psr7Factory::toPsr7Request(local raw HTTP/1.1 request bytes); method, URI, version, and headers`
- **Documentation:** [API reference](<https://github.com/alexpts/php-http-message-parser/blob/8eddf828b2e22e28b83d58658bee58d42834eef6/src/Factory/Psr7Factory.php>)
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

Native parser creating a PSR-7 request. PHP 8.5 emits deprecation notices when logging is enabled.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
