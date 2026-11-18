# guzzle/guzzle — HTTP/1.1 / PHP

- **Pinned release:** `v3.9.3`
- **Upstream:** [source repository](<https://github.com/guzzle/guzzle3>) · [Packagist](<https://packagist.org/packages/guzzle/guzzle>)
- **License:** MIT
- **Parsed scope:** single valid GET request line and Host, X-Parsarium, Connection headers
- **Underlying family:** Guzzle 3 HTTP message parser
- **Local input API:** `RequestFactory::fromMessage(local raw HTTP/1.1 bytes); request line, target, version, headers`
- **Documentation:** [API reference](<https://github.com/guzzle/guzzle3/blob/0645b70d953bc1c067bbc8d5bc53194706b628d9/src/Guzzle/Http/Message/RequestFactory.php>)
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

Monolithic Guzzle 3 release bundles the same parser lineage as guzzle/parser and guzzle/http.

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/php/guzzle_guzzle/README.md)

```sh
python3 parsarium.py build http11 php guzzle_guzzle
python3 parsarium.py run http11 php guzzle_guzzle controls/http11/request.http
```
