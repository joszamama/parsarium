# wahern-dns — DNS / C

Pinned release: `rel-20160808`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/c/wahern-dns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns c wahern-dns
python3 parsarium.py run dns c wahern-dns controls/dns/response.bin
python3 parsarium.py replay dns c wahern-dns CORPUS_DIR runs/dns-wahern-dns-replay
python3 parsarium.py afl build dns c wahern-dns
python3 parsarium.py afl prepare dns c wahern-dns runs/dns-wahern-dns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
