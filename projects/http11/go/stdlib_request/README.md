# net/http.ReadRequest(*bufio.Reader) — HTTP/1.1 / Go

Pinned release: `1.27.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[Standard API inventory](../../../../data/go/http11/standard.json)

## Run from the repository root

```sh
python3 parsarium.py build http11 go stdlib_request
python3 parsarium.py run http11 go stdlib_request controls/http11/request.http
python3 parsarium.py replay http11 go stdlib_request CORPUS_DIR runs/http11-stdlib_request-replay
python3 parsarium.py afl build http11 go stdlib_request
python3 parsarium.py afl prepare http11 go stdlib_request runs/http11-stdlib_request-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
