# dnslib — DNS / Java

Pinned release: `0.2.20`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/java/dnslib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns java sidn_dnslib
python3 parsarium.py run dns java sidn_dnslib controls/dns/response.bin
python3 parsarium.py replay dns java sidn_dnslib CORPUS_DIR runs/dns-sidn_dnslib-replay
python3 parsarium.py afl build dns java sidn_dnslib
python3 parsarium.py afl prepare dns java sidn_dnslib runs/dns-sidn_dnslib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
