# http-headers — HTTP/1.1 / JavaScript

Pinned release: `3.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/javascript/http-headers/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 javascript http_headers
python3 parsarium.py run http11 javascript http_headers controls/http11/request.http
python3 parsarium.py replay http11 javascript http_headers CORPUS_DIR runs/http11-http_headers-replay
python3 parsarium.py afl build http11 javascript http_headers
python3 parsarium.py afl prepare http11 javascript http_headers runs/http11-http_headers-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
