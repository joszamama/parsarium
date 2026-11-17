# dpkt — DNS / Python

Pinned release: `1.9.8`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/python/dpkt/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns python dpkt
python3 parsarium.py run dns python dpkt controls/dns/response.bin
python3 parsarium.py replay dns python dpkt CORPUS_DIR runs/dns-dpkt-replay
python3 parsarium.py afl build dns python dpkt
python3 parsarium.py afl prepare dns python dpkt runs/dns-dpkt-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
