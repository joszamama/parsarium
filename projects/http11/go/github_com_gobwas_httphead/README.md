# github.com/gobwas/httphead — HTTP/1.1 / Go

Pinned release: `v0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/go/github-com-gobwas-httphead/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 go github_com_gobwas_httphead
python3 parsarium.py run http11 go github_com_gobwas_httphead controls/http11/request.http
python3 parsarium.py replay http11 go github_com_gobwas_httphead CORPUS_DIR runs/http11-github_com_gobwas_httphead-replay
python3 parsarium.py afl build http11 go github_com_gobwas_httphead
python3 parsarium.py afl prepare http11 go github_com_gobwas_httphead runs/http11-github_com_gobwas_httphead-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
