# rawhttp-core — HTTP/1.1 / Java

Pinned release: `2.6.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/java/rawhttp-core/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 java rawhttp_core
python3 parsarium.py run http11 java rawhttp_core controls/http11/request.http
python3 parsarium.py replay http11 java rawhttp_core CORPUS_DIR runs/http11-rawhttp_core-replay
python3 parsarium.py afl build http11 java rawhttp_core
python3 parsarium.py afl prepare http11 java rawhttp_core runs/http11-rawhttp_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
