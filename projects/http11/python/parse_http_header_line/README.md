# parse-http-header-line — HTTP/1.1 / Python

Pinned release: `0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/python/parse-http-header-line/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 python parse_http_header_line
python3 parsarium.py run http11 python parse_http_header_line controls/http11/request.http
python3 parsarium.py replay http11 python parse_http_header_line CORPUS_DIR runs/http11-parse_http_header_line-replay
python3 parsarium.py afl build http11 python parse_http_header_line
python3 parsarium.py afl prepare http11 python parse_http_header_line runs/http11-parse_http_header_line-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
