# mitmproxy — DNS / Python

Pinned release: `12.3.1`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/python/mitmproxy/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns python mitmproxy
python3 parsarium.py run dns python mitmproxy controls/dns/response.bin
python3 parsarium.py replay dns python mitmproxy CORPUS_DIR runs/dns-mitmproxy-replay
python3 parsarium.py afl build dns python mitmproxy
python3 parsarium.py afl prepare dns python mitmproxy runs/dns-mitmproxy-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
