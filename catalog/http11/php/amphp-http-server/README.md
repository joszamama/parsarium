# amphp/http-server — HTTP/1.1 / PHP

- **Pinned release:** `v3.4.8`
- **Upstream:** [source repository](<https://github.com/amphp/http-server>) · [Packagist](<https://packagist.org/packages/amphp/http-server>)
- **License:** MIT
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** Amp native HTTP server parser
- **Local input API:** `SocketHttpServer::expose(local loopback socket); RequestHandler receives parsed HTTP/1.1 method, target, version, headers`
- **Documentation:** [API reference](<https://github.com/amphp/http-server/blob/31b004bf1cfd3feed3f0bdf20ddb9bfef935efb8/README.md>)
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

Pinned Amp HTTP server parses the saved raw request over a local TCP byte stream.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/php/amphp_http_server/README.md)

```sh
python3 parsarium.py build http11 php amphp_http_server
python3 parsarium.py run http11 php amphp_http_server controls/http11/request.http
```
