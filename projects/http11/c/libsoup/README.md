# libsoup — HTTP/1.1 / C

Pinned release: `3.8.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/c/libsoup/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 c libsoup
python3 parsarium.py run http11 c libsoup controls/http11/request.http
python3 parsarium.py replay http11 c libsoup CORPUS_DIR runs/http11-libsoup-replay
python3 parsarium.py afl build http11 c libsoup
python3 parsarium.py afl prepare http11 c libsoup runs/http11-libsoup-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
