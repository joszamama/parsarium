# httptools — HTTP/1.1 / Python

Pinned release: `0.9.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/python/httptools/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 python httptools
python3 parsarium.py run http11 python httptools controls/http11/request.http
python3 parsarium.py replay http11 python httptools CORPUS_DIR runs/http11-httptools-replay
python3 parsarium.py afl build http11 python httptools
python3 parsarium.py afl prepare http11 python httptools runs/http11-httptools-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
