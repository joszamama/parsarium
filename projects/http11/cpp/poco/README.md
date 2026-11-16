# poco — HTTP/1.1 / C++

Pinned release: `1.15.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/cpp/poco/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 cpp poco
python3 parsarium.py run http11 cpp poco controls/http11/request.http
python3 parsarium.py replay http11 cpp poco CORPUS_DIR runs/http11-poco-replay
python3 parsarium.py afl build http11 cpp poco
python3 parsarium.py afl prepare http11 cpp poco runs/http11-poco-afl
```

Replace `CORPUS_DIR` with a directory of HTTP/1.1 request files. The AFL++ command prepares a seeded run; it does not start a campaign.
