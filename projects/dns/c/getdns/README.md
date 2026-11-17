# getdns — DNS / C

Pinned release: `1.7.3`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/c/getdns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns c getdns
python3 parsarium.py run dns c getdns controls/dns/response.bin
python3 parsarium.py replay dns c getdns CORPUS_DIR runs/dns-getdns-replay
python3 parsarium.py afl build dns c getdns
python3 parsarium.py afl prepare dns c getdns runs/dns-getdns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
