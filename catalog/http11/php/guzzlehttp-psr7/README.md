# guzzlehttp/psr7 — HTTP/1.1 / PHP

- **Pinned release:** `3.3.0`
- **License:** MIT
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** Guzzle PSR-7 HTTP message parser
- **Local input API:** `Message::parseRequest(local raw HTTP/1.1 request bytes); method, target, version, and headers`
- **Documentation:** [API reference](<https://github.com/guzzle/psr7/blob/8b0a7e7db965a687eebe18333a128edac95db246/src/Message.php>)
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

Modern Guzzle PSR-7 parser; RingCentral and Workerman fork an older Guzzle PSR-7 implementation, so the lineage is shared.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/php/guzzle_psr7/README.md)

```sh
python3 parsarium.py build http11 php guzzle_psr7
python3 parsarium.py run http11 php guzzle_psr7 controls/http11/request.http
```
