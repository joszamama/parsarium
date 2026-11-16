# github.com/FastTLS/oohttp — HTTP/1.1 / Go

Pinned release: `v0.0.0-20261026180050-43186effd7f4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/go/github-com-fasttls-oohttp/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 go github_com_fasttls_oohttp
python3 parsarium.py run http11 go github_com_fasttls_oohttp controls/http11/request.http
python3 parsarium.py replay http11 go github_com_fasttls_oohttp CORPUS_DIR runs/http11-github_com_fasttls_oohttp-replay
python3 parsarium.py afl build http11 go github_com_fasttls_oohttp
python3 parsarium.py afl prepare http11 go github_com_fasttls_oohttp runs/http11-github_com_fasttls_oohttp-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
