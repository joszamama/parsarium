# github.com/antlabs/fio/http — HTTP/1.1 / Go

Pinned release: `v0.2.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/go/github-com-antlabs-fio-http/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 go github_com_antlabs_fio_http
python3 parsarium.py run http11 go github_com_antlabs_fio_http controls/http11/request.http
python3 parsarium.py replay http11 go github_com_antlabs_fio_http CORPUS_DIR runs/http11-github_com_antlabs_fio_http-replay
python3 parsarium.py afl build http11 go github_com_antlabs_fio_http
python3 parsarium.py afl prepare http11 go github_com_antlabs_fio_http runs/http11-github_com_antlabs_fio_http-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
