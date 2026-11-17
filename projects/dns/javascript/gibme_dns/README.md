# @gibme/dns — DNS / JavaScript

Pinned release: `22.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/javascript/gibme-dns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns javascript gibme_dns
python3 parsarium.py run dns javascript gibme_dns controls/dns/response.bin
python3 parsarium.py replay dns javascript gibme_dns CORPUS_DIR runs/dns-gibme_dns-replay
python3 parsarium.py afl build dns javascript gibme_dns
python3 parsarium.py afl prepare dns javascript gibme_dns runs/dns-gibme_dns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Two valid controls (a query and a response with CNAME, A, AAAA and MX answers). They do not establish EDNS0, DNSSEC, TXT or authority/additional behaviour.
