# react/dns — DNS / PHP

Pinned release: `v1.14.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/php/react-dns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns php react_dns
python3 parsarium.py run dns php react_dns controls/dns/response.bin
python3 parsarium.py replay dns php react_dns CORPUS_DIR runs/dns-react_dns-replay
python3 parsarium.py afl build dns php react_dns
python3 parsarium.py afl prepare dns php react_dns runs/dns-react_dns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
