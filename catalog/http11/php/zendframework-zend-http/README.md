# zendframework/zend-http — HTTP/1.1 / PHP

- **Pinned release:** `2.11.2`
- **License:** BSD-3-Clause
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** Zend/Laminas HTTP message parser lineage
- **Local input API:** `Request::fromString(local raw HTTP/1.1 bytes); request line, target, version, headers`
- **Documentation:** [API reference](<https://github.com/zendframework/zend-http/blob/e15e0ce45a2a4f642cd0b7b4f4d4d0366b729a1a/src/Request.php>)
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

Zend predecessor of laminas/laminas-http; shared request parser lineage.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/php/zendframework_zend_http/README.md)

```sh
python3 parsarium.py build http11 php zendframework_zend_http
python3 parsarium.py run http11 php zendframework_zend_http controls/http11/request.http
```
