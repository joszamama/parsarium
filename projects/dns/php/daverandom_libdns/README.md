# daverandom/libdns — DNS / PHP

Pinned release: `v2.1.0`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/php/daverandom-libdns/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns php daverandom_libdns
python3 parsarium.py run dns php daverandom_libdns controls/dns/response.bin
python3 parsarium.py replay dns php daverandom_libdns CORPUS_DIR runs/dns-daverandom_libdns-replay
python3 parsarium.py afl build dns php daverandom_libdns
python3 parsarium.py afl prepare dns php daverandom_libdns runs/dns-daverandom_libdns-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
