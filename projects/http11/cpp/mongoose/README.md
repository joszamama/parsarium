# mongoose — HTTP/1.1 / C++

Pinned release: `7.23`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/cpp/mongoose/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 cpp mongoose
python3 parsarium.py run http11 cpp mongoose controls/http11/request.http
python3 parsarium.py replay http11 cpp mongoose CORPUS_DIR runs/http11-mongoose-replay
python3 parsarium.py afl build http11 cpp mongoose
python3 parsarium.py afl prepare http11 cpp mongoose runs/http11-mongoose-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
