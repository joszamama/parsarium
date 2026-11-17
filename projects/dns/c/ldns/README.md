# ldns — DNS / C

Pinned release: `1.8.4`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/c/ldns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns c ldns
python3 parsarium.py run dns c ldns controls/dns/response.bin
python3 parsarium.py replay dns c ldns CORPUS_DIR runs/dns-ldns-replay
python3 parsarium.py afl build dns c ldns
python3 parsarium.py afl prepare dns c ldns runs/dns-ldns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
