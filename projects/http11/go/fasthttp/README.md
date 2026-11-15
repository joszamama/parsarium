# github.com/valyala/fasthttp — HTTP/1.1 / Go

Pinned release: `v1.78.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/go/github-com-valyala-fasthttp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 go fasthttp
python3 parsarium.py run http11 go fasthttp controls/http11/request.http
python3 parsarium.py replay http11 go fasthttp CORPUS_DIR runs/http11-fasthttp-replay
python3 parsarium.py afl build http11 go fasthttp
python3 parsarium.py afl prepare http11 go fasthttp runs/http11-fasthttp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
