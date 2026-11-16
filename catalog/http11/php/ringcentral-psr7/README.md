# ringcentral/psr7 — HTTP/1.1 / PHP

- **Pinned release:** `1.3.0`
- **License:** MIT
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** Guzzle PSR-7 HTTP message parser
- **Local input API:** `RingCentral\Psr7\parse_request(local raw HTTP/1.1 bytes); request line, target, version, headers`
- **Documentation:** [API reference](<https://github.com/ringcentral/psr7/blob/360faaec4b563958b673fb52bbe94e37f14bc686/README.md>)
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

Fork of older Guzzle PSR-7 code; shared parser lineage with workerman/psr7 and guzzlehttp/psr7.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/php/ringcentral_psr7/README.md)

```sh
python3 parsarium.py build http11 php ringcentral_psr7
python3 parsarium.py run http11 php ringcentral_psr7 controls/http11/request.http
```
