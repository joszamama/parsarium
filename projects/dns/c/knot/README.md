# knot — DNS / C

Pinned release: `3.6.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/c/knot/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns c knot
python3 parsarium.py run dns c knot controls/dns/response.bin
python3 parsarium.py replay dns c knot CORPUS_DIR runs/dns-knot-replay
python3 parsarium.py afl build dns c knot
python3 parsarium.py afl prepare dns c knot runs/dns-knot-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
