# llhttp — HTTP/1.1 / C++

Pinned release: `9.4.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/cpp/llhttp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 cpp llhttp
python3 parsarium.py run http11 cpp llhttp controls/http11/request.http
python3 parsarium.py replay http11 cpp llhttp CORPUS_DIR runs/http11-llhttp-replay
python3 parsarium.py afl build http11 cpp llhttp
python3 parsarium.py afl prepare http11 cpp llhttp runs/http11-llhttp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
