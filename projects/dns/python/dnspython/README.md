# dnspython — DNS / Python

Pinned release: `2.9.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/python/dnspython/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns python dnspython
python3 parsarium.py run dns python dnspython controls/dns/response.bin
python3 parsarium.py replay dns python dnspython CORPUS_DIR runs/dns-dnspython-replay
python3 parsarium.py afl build dns python dnspython
python3 parsarium.py afl prepare dns python dnspython runs/dns-dnspython-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
