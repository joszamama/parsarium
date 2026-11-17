# h2o — HTTP/1.1 / C++

Pinned release: `2.2.6`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/cpp/h2o/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 cpp h2o
python3 parsarium.py run http11 cpp h2o controls/http11/request.http
python3 parsarium.py replay http11 cpp h2o CORPUS_DIR runs/http11-h2o-replay
python3 parsarium.py afl build http11 cpp h2o
python3 parsarium.py afl prepare http11 cpp h2o runs/http11-h2o-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
