# httpp — HTTP/1.1 / C

Pinned release: `2.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/c/httpp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 c httpp
python3 parsarium.py run http11 c httpp controls/http11/request.http
python3 parsarium.py replay http11 c httpp CORPUS_DIR runs/http11-httpp-replay
python3 parsarium.py afl build http11 c httpp
python3 parsarium.py afl prepare http11 c httpp runs/http11-httpp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
