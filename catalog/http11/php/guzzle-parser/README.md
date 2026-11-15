# guzzle/parser — HTTP/1.1 / PHP

- **Pinned release:** `v3.9.2`
- **License:** MIT
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** Guzzle 3 HTTP message parser
- **Local input API:** `MessageParser::parseRequest(local raw HTTP/1.1 request bytes); request line, URI, version, and headers`
- **Documentation:** [API reference](<https://github.com/Guzzle3/parser/blob/6874d171318a8e93eb6d224cf85e4678490b625c/Guzzle/Parser/Message/MessageParser.php>)
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

Older Guzzle 3 parser implementation; Composer package is abandoned, but its pinned release passed.

## Runnable harness

A Docker harness with parser-source coverage has not yet been verified for this API path.
