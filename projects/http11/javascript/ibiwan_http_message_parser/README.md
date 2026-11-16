# @ibiwan/http-message-parser — HTTP/1.1 / JavaScript

Pinned release: `0.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/javascript/ibiwan-http-message-parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 javascript ibiwan_http_message_parser
python3 parsarium.py run http11 javascript ibiwan_http_message_parser controls/http11/request.http
python3 parsarium.py replay http11 javascript ibiwan_http_message_parser CORPUS_DIR runs/http11-ibiwan_http_message_parser-replay
python3 parsarium.py afl build http11 javascript ibiwan_http_message_parser
python3 parsarium.py afl prepare http11 javascript ibiwan_http_message_parser runs/http11-ibiwan_http_message_parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
