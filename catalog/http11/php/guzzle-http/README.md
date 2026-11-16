# guzzle/http — HTTP/1.1 / PHP

- **Pinned release:** `v3.9.2`
- **License:** MIT
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** Guzzle 3 HTTP message parser
- **Local input API:** `RequestFactory::fromMessage(local raw HTTP/1.1 bytes); request line, target, version, headers`
- **Documentation:** [API reference](<https://github.com/Guzzle3/http/blob/1e8dd1e2ba9dc42332396f39fbfab950b2301dc5/Guzzle/Http/Message/RequestFactory.php>)
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

Package factory delegates to pinned guzzle/parser dependency; shared underlying parser implementation.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/php/guzzle_http/README.md)

```sh
python3 parsarium.py build http11 php guzzle_http
python3 parsarium.py run http11 php guzzle_http controls/http11/request.http
```
