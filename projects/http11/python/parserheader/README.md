# parserheader — HTTP/1.1 / Python

Pinned release: `0.38.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/python/parserheader/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 python parserheader
python3 parsarium.py run http11 python parserheader controls/http11/request.http
python3 parsarium.py replay http11 python parserheader CORPUS_DIR runs/http11-parserheader-replay
python3 parsarium.py afl build http11 python parserheader
python3 parsarium.py afl prepare http11 python parserheader runs/http11-parserheader-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
