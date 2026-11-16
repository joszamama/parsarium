# @alikia/http-parser — HTTP/1.1 / JavaScript

Pinned release: `1.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/javascript/alikia-http-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 javascript alikia_http_parser
python3 parsarium.py run http11 javascript alikia_http_parser controls/http11/request.http
python3 parsarium.py replay http11 javascript alikia_http_parser CORPUS_DIR runs/http11-alikia_http_parser-replay
python3 parsarium.py afl build http11 javascript alikia_http_parser
python3 parsarium.py afl prepare http11 javascript alikia_http_parser runs/http11-alikia_http_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
