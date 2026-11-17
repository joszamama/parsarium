# github.com/benburkert/dns — DNS / Go

Pinned release: `v0.0.0-20190225204957-d356cf78cdfc`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/go/github-com-benburkert-dns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns go github_com_benburkert_dns
python3 parsarium.py run dns go github_com_benburkert_dns controls/dns/response.bin
python3 parsarium.py replay dns go github_com_benburkert_dns CORPUS_DIR runs/dns-github_com_benburkert_dns-replay
python3 parsarium.py afl build dns go github_com_benburkert_dns
python3 parsarium.py afl prepare dns go github_com_benburkert_dns runs/dns-github_com_benburkert_dns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
