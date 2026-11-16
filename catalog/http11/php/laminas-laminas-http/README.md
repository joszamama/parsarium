# laminas/laminas-http — HTTP/1.1 / PHP

- **Pinned release:** `2.23.0`
- **License:** BSD-3-Clause
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** Zend/Laminas HTTP message parser lineage
- **Local input API:** `Request::fromString(local raw HTTP/1.1 request bytes); method, URI, version, and headers`
- **Documentation:** [API reference](<https://github.com/laminas/laminas-http/blob/9462fc84330d25b23383823831380abb33907fdd/src/Request.php>)
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

Laminas continuation of Zend HTTP; shared request parser lineage with zendframework/zend-http.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/php/laminas_laminas_http/README.md)

```sh
python3 parsarium.py build http11 php laminas_laminas_http
python3 parsarium.py run http11 php laminas_laminas_http controls/http11/request.http
```
