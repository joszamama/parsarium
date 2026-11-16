# github.com/antlabs/httparser — HTTP/1.1 / Go

Pinned release: `v0.0.11`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/go/github-com-antlabs-httparser/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 go github_com_antlabs_httparser
python3 parsarium.py run http11 go github_com_antlabs_httparser controls/http11/request.http
python3 parsarium.py replay http11 go github_com_antlabs_httparser CORPUS_DIR runs/http11-github_com_antlabs_httparser-replay
python3 parsarium.py afl build http11 go github_com_antlabs_httparser
python3 parsarium.py afl prepare http11 go github_com_antlabs_httparser runs/http11-github_com_antlabs_httparser-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
