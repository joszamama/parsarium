# github.com/hsiafan/httpdump/httpport — HTTP/1.1 / Go

Pinned release: `v0.0.0-20231019014708-4fd809447b59`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/http11/go/github-com-hsiafan-httpdump-httpport/README.md)

## Run from the repository root

```sh
python3 parsarium.py build http11 go github_com_hsiafan_httpdump_httpport
python3 parsarium.py run http11 go github_com_hsiafan_httpdump_httpport controls/http11/request.http
python3 parsarium.py replay http11 go github_com_hsiafan_httpdump_httpport CORPUS_DIR runs/http11-github_com_hsiafan_httpdump_httpport-replay
python3 parsarium.py afl build http11 go github_com_hsiafan_httpdump_httpport
python3 parsarium.py afl prepare http11 go github_com_hsiafan_httpdump_httpport runs/http11-github_com_hsiafan_httpdump_httpport-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
