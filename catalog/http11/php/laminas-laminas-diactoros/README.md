# laminas/laminas-diactoros — HTTP/1.1 / PHP

- **Pinned release:** `3.10.0`
- **Upstream:** [source repository](<https://github.com/laminas/laminas-diactoros>) · [Packagist](<https://packagist.org/packages/laminas/laminas-diactoros>)
- **License:** BSD-3-Clause
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** Diactoros HTTP message parser lineage
- **Local input API:** `Request\Serializer::fromString(local raw HTTP/1.1 bytes); request line, target, version, headers`
- **Documentation:** [API reference](<https://github.com/laminas/laminas-diactoros/blob/5939fbc03e9043e5d27050ed584de263b869c57f/src/Request/Serializer.php>)
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

Laminas descendant of Phly/Zend Diactoros request serializer; shared family lineage with phly/http.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/php/laminas_laminas_diactoros/README.md)

```sh
python3 parsarium.py build http11 php laminas_laminas_diactoros
python3 parsarium.py run http11 php laminas_laminas_diactoros controls/http11/request.http
```
