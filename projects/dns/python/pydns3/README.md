# pydns3 — DNS / Python

Pinned release: `0.0.10`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/python/pydns3/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns python pydns3
python3 parsarium.py run dns python pydns3 controls/dns/response.bin
python3 parsarium.py replay dns python pydns3 CORPUS_DIR runs/dns-pydns3-replay
python3 parsarium.py afl build dns python pydns3
python3 parsarium.py afl prepare dns python pydns3 runs/dns-pydns3-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
