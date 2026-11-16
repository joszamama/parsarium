# h1parser — HTTP/1.1 / Python

Pinned release: `0.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/python/h1parser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 python h1parser
python3 parsarium.py run http11 python h1parser controls/http11/request.http
python3 parsarium.py replay http11 python h1parser CORPUS_DIR runs/http11-h1parser-replay
python3 parsarium.py afl build http11 python h1parser
python3 parsarium.py afl prepare http11 python h1parser runs/http11-h1parser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
