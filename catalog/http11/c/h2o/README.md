# h2o — HTTP/1.1 / C

- **Pinned release:** `2.2.6`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 GET request method, target, version and headers from local byte buffer via H2O-bundled parser
- **Underlying family:** H2O 2.2.6 bundles PicoHTTPParser as its HTTP/1 parser; separate tagged H2O package distribution but same underlying parser family as h2o/picohttpparser 1.5, not an independent engine
- **Local input API:** `H2O-bundled PicoHTTPParser phr_parse_request(local request bytes, length, method, path, version, headers); the pinned H2O distribution documents and ships the C API`
- **Documentation:** [API reference](<https://github.com/h2o/h2o/blob/v2.2.6/deps/picohttpparser/README.md>)
- **Catalog evidence:** [parser record](../../../../data/c/http11/parsers.json) · [control verification](../../../../data/c/http11/verification.json) · [within-ecosystem ranking](../../../../data/c/http11/ranking.md)
- **Valid control:** [`controls/http11/request.http`](../../../../controls/http11/request.http)

## Observed control result

```json
{
  "method": "GET",
  "path": "/parsarium?x=1",
  "version": "1.1"
}
```

## Run this target

[Docker harness and verification receipt](../../../../projects/http11/c/h2o/README.md)

```sh
python3 parsarium.py build http11 c h2o
python3 parsarium.py run http11 c h2o controls/http11/request.http
```
