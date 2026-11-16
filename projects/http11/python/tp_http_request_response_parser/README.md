# tp-http-request-response-parser — HTTP/1.1 / Python

Pinned release: `2026.5.18`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/python/tp-http-request-response-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 python tp_http_request_response_parser
python3 parsarium.py run http11 python tp_http_request_response_parser controls/http11/request.http
python3 parsarium.py replay http11 python tp_http_request_response_parser CORPUS_DIR runs/http11-tp_http_request_response_parser-replay
python3 parsarium.py afl build http11 python tp_http_request_response_parser
python3 parsarium.py afl prepare http11 python tp_http_request_response_parser runs/http11-tp_http_request_response_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
