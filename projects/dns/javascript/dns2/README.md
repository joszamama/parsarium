# dns2 — DNS / JavaScript

Pinned release: `3.1.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/javascript/dns2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns javascript dns2
python3 parsarium.py run dns javascript dns2 controls/dns/response.bin
python3 parsarium.py replay dns javascript dns2 CORPUS_DIR runs/dns-dns2-replay
python3 parsarium.py afl build dns javascript dns2
python3 parsarium.py afl prepare dns javascript dns2 runs/dns-dns2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.

**Coverage limit:** Two valid controls (a query and a response with CNAME, A, AAAA and MX answers). They do not establish EDNS0, DNSSEC, TXT or authority/additional behaviour.
