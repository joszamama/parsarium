# picohttpparser — HTTP/1.1 / C

- **Pinned release:** `1.5`
- **License:** MIT
- **Parsed scope:** HTTP/1.1 GET request method, target and version after complete header parse
- **Underlying family:** PicoHTTPParser C request parser, used by H2O
- **Local input API:** `phr_parse_request(local request bytes, length, method/path/version/header outputs)`
- **Documentation:** [API reference](<https://github.com/h2o/picohttpparser#phr_parse_request>)
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

[Docker harness and verification receipt](../../../../projects/http11/c/picohttpparser/README.md)

```sh
python3 parsarium.py build http11 c picohttpparser
python3 parsarium.py run http11 c picohttpparser controls/http11/request.http
```
