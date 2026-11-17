# hbo-dnsd — DNS / JavaScript

Pinned release: `0.9.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/javascript/hbo-dnsd/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns javascript hbo_dnsd
python3 parsarium.py run dns javascript hbo_dnsd controls/dns/response.bin
python3 parsarium.py replay dns javascript hbo_dnsd CORPUS_DIR runs/dns-hbo_dnsd-replay
python3 parsarium.py afl build dns javascript hbo_dnsd
python3 parsarium.py afl prepare dns javascript hbo_dnsd runs/dns-hbo_dnsd-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Two valid controls (a query and a response with CNAME, A, AAAA and MX answers). They do not establish EDNS0, DNSSEC, TXT or authority/additional behaviour.
