# github.com/cznic/dns/msg — DNS / Go

Pinned release: `v0.0.0-20181122101858-8a2913d6a50b`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/go/github-com-cznic-dns-msg/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns go github_com_cznic_dns_msg
python3 parsarium.py run dns go github_com_cznic_dns_msg controls/dns/response.bin
python3 parsarium.py replay dns go github_com_cznic_dns_msg CORPUS_DIR runs/dns-github_com_cznic_dns_msg-replay
python3 parsarium.py afl build dns go github_com_cznic_dns_msg
python3 parsarium.py afl prepare dns go github_com_cznic_dns_msg runs/dns-github_com_cznic_dns_msg-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
