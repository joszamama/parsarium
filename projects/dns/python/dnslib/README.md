# dnslib — DNS / Python

Pinned release: `0.9.26`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/python/dnslib/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns python dnslib
python3 parsarium.py run dns python dnslib controls/dns/response.bin
python3 parsarium.py replay dns python dnslib CORPUS_DIR runs/dns-dnslib-replay
python3 parsarium.py afl build dns python dnslib
python3 parsarium.py afl prepare dns python dnslib runs/dns-dnslib-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
