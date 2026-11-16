# http-z — HTTP/1.1 / JavaScript

Pinned release: `8.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/javascript/http-z/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 javascript http_z
python3 parsarium.py run http11 javascript http_z controls/http11/request.http
python3 parsarium.py replay http11 javascript http_z CORPUS_DIR runs/http11-http_z-replay
python3 parsarium.py afl build http11 javascript http_z
python3 parsarium.py afl prepare http11 javascript http_z runs/http11-http_z-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
