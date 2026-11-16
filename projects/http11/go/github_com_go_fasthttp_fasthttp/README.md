# github.com/go-fasthttp/fasthttp — HTTP/1.1 / Go

Pinned release: `v0.0.0-20161128095036-1c39678a4dd0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/go/github-com-go-fasthttp-fasthttp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 go github_com_go_fasthttp_fasthttp
python3 parsarium.py run http11 go github_com_go_fasthttp_fasthttp controls/http11/request.http
python3 parsarium.py replay http11 go github_com_go_fasthttp_fasthttp CORPUS_DIR runs/http11-github_com_go_fasthttp_fasthttp-replay
python3 parsarium.py afl build http11 go github_com_go_fasthttp_fasthttp
python3 parsarium.py afl prepare http11 go github_com_go_fasthttp_fasthttp runs/http11-github_com_go_fasthttp_fasthttp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
