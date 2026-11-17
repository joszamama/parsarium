# github.com/phuslu/fastdns — DNS / Go

Pinned release: `v0.17.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/go/github-com-phuslu-fastdns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns go github_com_phuslu_fastdns
python3 parsarium.py run dns go github_com_phuslu_fastdns controls/dns/response.bin
python3 parsarium.py replay dns go github_com_phuslu_fastdns CORPUS_DIR runs/dns-github_com_phuslu_fastdns-replay
python3 parsarium.py afl build dns go github_com_phuslu_fastdns
python3 parsarium.py afl prepare dns go github_com_phuslu_fastdns runs/dns-github_com_phuslu_fastdns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
