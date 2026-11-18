# namespy — DNS / Python

Pinned release: `0.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/python/namespy/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns python namespy
python3 parsarium.py run dns python namespy controls/dns/response.bin
python3 parsarium.py replay dns python namespy CORPUS_DIR runs/dns-namespy-replay
python3 parsarium.py afl build dns python namespy
python3 parsarium.py afl prepare dns python namespy runs/dns-namespy-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
