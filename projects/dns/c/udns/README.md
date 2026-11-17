# udns — DNS / C

Pinned release: `0.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/c/udns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns c udns
python3 parsarium.py run dns c udns controls/dns/response.bin
python3 parsarium.py replay dns c udns CORPUS_DIR runs/dns-udns-replay
python3 parsarium.py afl build dns c udns
python3 parsarium.py afl prepare dns c udns runs/dns-udns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
