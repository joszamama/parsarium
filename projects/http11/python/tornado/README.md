# tornado — HTTP/1.1 / Python

Pinned release: `6.6.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/python/tornado/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 python tornado
python3 parsarium.py run http11 python tornado controls/http11/response.http
python3 parsarium.py replay http11 python tornado CORPUS_DIR runs/http11-tornado-replay
python3 parsarium.py afl build http11 python tornado
python3 parsarium.py afl prepare http11 python tornado runs/http11-tornado-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
