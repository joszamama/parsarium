# Twisted — HTTP/1.1 / Python

Pinned release: `26.10.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/python/twisted/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 python twisted
python3 parsarium.py run http11 python twisted controls/http11/request.http
python3 parsarium.py replay http11 python twisted CORPUS_DIR runs/http11-twisted-replay
python3 parsarium.py afl build http11 python twisted
python3 parsarium.py afl prepare http11 python twisted runs/http11-twisted-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
