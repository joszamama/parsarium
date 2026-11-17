# twisted — DNS / Python

Pinned release: `26.10.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/python/twisted/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns python twisted
python3 parsarium.py run dns python twisted controls/dns/response.bin
python3 parsarium.py replay dns python twisted CORPUS_DIR runs/dns-twisted-replay
python3 parsarium.py afl build dns python twisted
python3 parsarium.py afl prepare dns python twisted runs/dns-twisted-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
