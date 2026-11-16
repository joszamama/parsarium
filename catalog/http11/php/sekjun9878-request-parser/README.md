# sekjun9878/request-parser — HTTP/1.1 / PHP

- **Pinned release:** `v1.0.1`
- **License:** MIT
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** Sekjun HTTP request parser
- **Local input API:** `RequestParser::addData(local raw HTTP/1.1 request bytes), Request::create; method, URI, version, and headers`
- **Documentation:** [API reference](<https://github.com/sekjun9878/request-parser/blob/8c32cf4c6b79fb0c5c59cbb589d59abb11a10dfc/README.md>)
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

Native incremental parser; PHP 8.5 emits deprecation notices when logging is enabled.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/php/sekjun9878_request_parser/README.md)

```sh
python3 parsarium.py build http11 php sekjun9878_request_parser
python3 parsarium.py run http11 php sekjun9878_request_parser controls/http11/request.http
```
