# github.com/sebishogun/simdhttp/http1 — HTTP/1.1 / Go

Pinned release: `v0.0.0-20261007210108-01268e016029`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/go/github-com-sebishogun-simdhttp-http1/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 go github_com_sebishogun_simdhttp_http1
python3 parsarium.py run http11 go github_com_sebishogun_simdhttp_http1 controls/http11/request.http
python3 parsarium.py replay http11 go github_com_sebishogun_simdhttp_http1 CORPUS_DIR runs/http11-github_com_sebishogun_simdhttp_http1-replay
python3 parsarium.py afl build http11 go github_com_sebishogun_simdhttp_http1
python3 parsarium.py afl prepare http11 go github_com_sebishogun_simdhttp_http1 runs/http11-github_com_sebishogun_simdhttp_http1-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
