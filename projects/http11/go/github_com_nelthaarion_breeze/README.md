# github.com/nelthaarion/breeze — HTTP/1.1 / Go

Pinned release: `v1.6.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/go/github-com-nelthaarion-breeze/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 go github_com_nelthaarion_breeze
python3 parsarium.py run http11 go github_com_nelthaarion_breeze controls/http11/request.http
python3 parsarium.py replay http11 go github_com_nelthaarion_breeze CORPUS_DIR runs/http11-github_com_nelthaarion_breeze-replay
python3 parsarium.py afl build http11 go github_com_nelthaarion_breeze
python3 parsarium.py afl prepare http11 go github_com_nelthaarion_breeze runs/http11-github_com_nelthaarion_breeze-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
