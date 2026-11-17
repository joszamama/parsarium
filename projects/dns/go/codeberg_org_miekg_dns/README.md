# codeberg.org/miekg/dns — DNS / Go

Pinned release: `v0.6.133`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/go/codeberg-org-miekg-dns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns go codeberg_org_miekg_dns
python3 parsarium.py run dns go codeberg_org_miekg_dns controls/dns/response.bin
python3 parsarium.py replay dns go codeberg_org_miekg_dns CORPUS_DIR runs/dns-codeberg_org_miekg_dns-replay
python3 parsarium.py afl build dns go codeberg_org_miekg_dns
python3 parsarium.py afl prepare dns go codeberg_org_miekg_dns runs/dns-codeberg_org_miekg_dns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
