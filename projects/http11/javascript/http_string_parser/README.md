# http-string-parser — HTTP/1.1 / JavaScript

Pinned release: `0.0.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/javascript/http-string-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 javascript http_string_parser
python3 parsarium.py run http11 javascript http_string_parser controls/http11/request.http
python3 parsarium.py replay http11 javascript http_string_parser CORPUS_DIR runs/http11-http_string_parser-replay
python3 parsarium.py afl build http11 javascript http_string_parser
python3 parsarium.py afl prepare http11 javascript http_string_parser runs/http11-http_string_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
