# c-ares — DNS / C

Pinned release: `1.34.9`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/c/c-ares/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns c c-ares
python3 parsarium.py run dns c c-ares controls/dns/response.bin
python3 parsarium.py replay dns c c-ares CORPUS_DIR runs/dns-c-ares-replay
python3 parsarium.py afl build dns c c-ares
python3 parsarium.py afl prepare dns c c-ares runs/dns-c-ares-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
