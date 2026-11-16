# libhv — HTTP/1.1 / C

Pinned release: `1.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/c/libhv/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 c libhv
python3 parsarium.py run http11 c libhv controls/http11/request.http
python3 parsarium.py replay http11 c libhv CORPUS_DIR runs/http11-libhv-replay
python3 parsarium.py afl build http11 c libhv
python3 parsarium.py afl prepare http11 c libhv runs/http11-libhv-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
