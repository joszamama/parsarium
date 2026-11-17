# dns4s-core_2.13 — DNS / Java

Pinned release: `0.21.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/java/dns4s-core-2-13/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns java dns4s_core
python3 parsarium.py run dns java dns4s_core controls/dns/response.bin
python3 parsarium.py replay dns java dns4s_core CORPUS_DIR runs/dns-dns4s_core-replay
python3 parsarium.py afl build dns java dns4s_core
python3 parsarium.py afl prepare dns java dns4s_core runs/dns-dns4s_core-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
