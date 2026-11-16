# vircom/http-parser — HTTP/1.1 / PHP

- **Pinned release:** `1.0.1`
- **License:** MIT
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** VirCom native HTTP message parser
- **Local input API:** `HttpParserFactory::createRequestParser()->parse(local raw HTTP/1.1 bytes); request line, target, version, headers`
- **Documentation:** [API reference](<https://github.com/vircom/http-parser/blob/9f3e1e9e375c4446510541be281e7f92f5013df2/README.md>)
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

Native request and header parser; pinned 1.0.1 requires PHP 7.4.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/php/vircom_http_parser/README.md)

```sh
python3 parsarium.py build http11 php vircom_http_parser
python3 parsarium.py run http11 php vircom_http_parser controls/http11/request.http
```
