# http-parser-ts — HTTP/1.1 / JavaScript

Pinned release: `0.1.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/javascript/http-parser-ts/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 javascript http_parser_ts
python3 parsarium.py run http11 javascript http_parser_ts controls/http11/request.http
python3 parsarium.py replay http11 javascript http_parser_ts CORPUS_DIR runs/http11-http_parser_ts-replay
python3 parsarium.py afl build http11 javascript http_parser_ts
python3 parsarium.py afl prepare http11 javascript http_parser_ts runs/http11-http_parser_ts-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
