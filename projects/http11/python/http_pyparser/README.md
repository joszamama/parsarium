# http-pyparser — HTTP/1.1 / Python

Pinned release: `0.5.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/python/http-pyparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 python http_pyparser
python3 parsarium.py run http11 python http_pyparser controls/http11/request.http
python3 parsarium.py replay http11 python http_pyparser CORPUS_DIR runs/http11-http_pyparser-replay
python3 parsarium.py afl build http11 python http_pyparser
python3 parsarium.py afl prepare http11 python http_pyparser runs/http11-http_pyparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
