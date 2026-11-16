# github.com/justIliane/blazehttp/pkg/header — HTTP/1.1 / Go

Pinned release: `v1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/go/github-com-justiliane-blazehttp-pkg-header/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 go github_com_justiliane_blazehttp_pkg_header
python3 parsarium.py run http11 go github_com_justiliane_blazehttp_pkg_header controls/http11/request.http
python3 parsarium.py replay http11 go github_com_justiliane_blazehttp_pkg_header CORPUS_DIR runs/http11-github_com_justiliane_blazehttp_pkg_header-replay
python3 parsarium.py afl build http11 go github_com_justiliane_blazehttp_pkg_header
python3 parsarium.py afl prepare http11 go github_com_justiliane_blazehttp_pkg_header runs/http11-github_com_justiliane_blazehttp_pkg_header-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
