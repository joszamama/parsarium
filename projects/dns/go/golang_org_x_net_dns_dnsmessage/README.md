# golang.org/x/net/dns/dnsmessage — DNS / Go

Pinned release: `v0.63.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/go/golang-org-x-net-dns-dnsmessage/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns go golang_org_x_net_dns_dnsmessage
python3 parsarium.py run dns go golang_org_x_net_dns_dnsmessage controls/dns/response.bin
python3 parsarium.py replay dns go golang_org_x_net_dns_dnsmessage CORPUS_DIR runs/dns-golang_org_x_net_dns_dnsmessage-replay
python3 parsarium.py afl build dns go golang_org_x_net_dns_dnsmessage
python3 parsarium.py afl prepare dns go golang_org_x_net_dns_dnsmessage runs/dns-golang_org_x_net_dns_dnsmessage-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
