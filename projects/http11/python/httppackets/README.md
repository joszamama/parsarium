# httppackets — HTTP/1.1 / Python

Pinned release: `0.1.0a0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/python/httppackets/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 python httppackets
python3 parsarium.py run http11 python httppackets controls/http11/request.http
python3 parsarium.py replay http11 python httppackets CORPUS_DIR runs/http11-httppackets-replay
python3 parsarium.py afl build http11 python httppackets
python3 parsarium.py afl prepare http11 python httppackets runs/http11-httppackets-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
