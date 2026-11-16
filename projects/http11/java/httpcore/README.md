# httpcore — HTTP/1.1 / Java

Pinned release: `4.4.16`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/java/httpcore/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 java httpcore
python3 parsarium.py run http11 java httpcore controls/http11/request.http
python3 parsarium.py replay http11 java httpcore CORPUS_DIR runs/http11-httpcore-replay
python3 parsarium.py afl build http11 java httpcore
python3 parsarium.py afl prepare http11 java httpcore runs/http11-httpcore-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
