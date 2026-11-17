# github.com/miekg/dns — DNS / Go

Pinned release: `v1.1.73`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/go/github-com-miekg-dns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns go github_com_miekg_dns
python3 parsarium.py run dns go github_com_miekg_dns controls/dns/response.bin
python3 parsarium.py replay dns go github_com_miekg_dns CORPUS_DIR runs/dns-github_com_miekg_dns-replay
python3 parsarium.py afl build dns go github_com_miekg_dns
python3 parsarium.py afl prepare dns go github_com_miekg_dns runs/dns-github_com_miekg_dns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
