# github.com/lesismal/nbio/nbhttp — HTTP/1.1 / Go

Pinned release: `v1.7.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/go/github-com-lesismal-nbio-nbhttp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 go github_com_lesismal_nbio_nbhttp
python3 parsarium.py run http11 go github_com_lesismal_nbio_nbhttp controls/http11/request.http
python3 parsarium.py replay http11 go github_com_lesismal_nbio_nbhttp CORPUS_DIR runs/http11-github_com_lesismal_nbio_nbhttp-replay
python3 parsarium.py afl build http11 go github_com_lesismal_nbio_nbhttp
python3 parsarium.py afl prepare http11 go github_com_lesismal_nbio_nbhttp runs/http11-github_com_lesismal_nbio_nbhttp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
