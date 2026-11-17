# dns-js — DNS / JavaScript

Pinned release: `0.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/javascript/dns-js/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns javascript dns_js
python3 parsarium.py run dns javascript dns_js controls/dns/response.bin
python3 parsarium.py replay dns javascript dns_js CORPUS_DIR runs/dns-dns_js-replay
python3 parsarium.py afl build dns javascript dns_js
python3 parsarium.py afl prepare dns javascript dns_js runs/dns-dns_js-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Two valid controls (a query and a response with CNAME, A, AAAA and MX answers). They do not establish EDNS0, DNSSEC, TXT or authority/additional behaviour.
