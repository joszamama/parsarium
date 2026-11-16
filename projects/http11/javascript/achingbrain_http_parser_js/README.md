# @achingbrain/http-parser-js — HTTP/1.1 / JavaScript

Pinned release: `0.5.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/javascript/achingbrain-http-parser-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 javascript achingbrain_http_parser_js
python3 parsarium.py run http11 javascript achingbrain_http_parser_js controls/http11/request.http
python3 parsarium.py replay http11 javascript achingbrain_http_parser_js CORPUS_DIR runs/http11-achingbrain_http_parser_js-replay
python3 parsarium.py afl build http11 javascript achingbrain_http_parser_js
python3 parsarium.py afl prepare http11 javascript achingbrain_http_parser_js runs/http11-achingbrain_http_parser_js-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
