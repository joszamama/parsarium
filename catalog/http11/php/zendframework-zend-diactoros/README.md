# zendframework/zend-diactoros — HTTP/1.1 / PHP

- **Pinned release:** `2.2.1`
- **License:** BSD-3-Clause
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** Diactoros HTTP message parser lineage
- **Local input API:** `Request\Serializer::fromString(local raw HTTP/1.1 bytes); request line, target, version, headers`
- **Documentation:** [API reference](<https://github.com/zendframework/zend-diactoros/blob/de5847b068362a88684a55b0dbb40d85986cfa52/src/Request/Serializer.php>)
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

Zend predecessor of Laminas Diactoros; shared serializer lineage with phly/http and laminas/laminas-diactoros.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/php/zendframework_zend_diactoros/README.md)

```sh
python3 parsarium.py build http11 php zendframework_zend_diactoros
python3 parsarium.py run http11 php zendframework_zend_diactoros controls/http11/request.http
```
