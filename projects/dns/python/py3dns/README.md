# py3dns — DNS / Python

Pinned release: `4.0.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/python/py3dns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns python py3dns
python3 parsarium.py run dns python py3dns controls/dns/response.bin
python3 parsarium.py replay dns python py3dns CORPUS_DIR runs/dns-py3dns-replay
python3 parsarium.py afl build dns python py3dns
python3 parsarium.py afl prepare dns python py3dns runs/dns-py3dns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
