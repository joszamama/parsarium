# pyasyncdns — DNS / Python

Pinned release: `1.0.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/python/pyasyncdns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns python pyasyncdns
python3 parsarium.py run dns python pyasyncdns controls/dns/response.bin
python3 parsarium.py replay dns python pyasyncdns CORPUS_DIR runs/dns-pyasyncdns-replay
python3 parsarium.py afl build dns python pyasyncdns
python3 parsarium.py afl prepare dns python pyasyncdns runs/dns-pyasyncdns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
