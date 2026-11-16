# amphp/http-server — HTTP/1.1 / PHP

Pinned release: `v3.4.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/php/amphp-http-server/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 php amphp_http_server
python3 parsarium.py run http11 php amphp_http_server controls/http11/request.http
python3 parsarium.py replay http11 php amphp_http_server CORPUS_DIR runs/http11-amphp_http_server-replay
python3 parsarium.py afl build http11 php amphp_http_server
python3 parsarium.py afl prepare http11 php amphp_http_server runs/http11-amphp_http_server-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
