# jdwx/dns-query — DNS / PHP

Pinned release: `v2.0.11`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/php/jdwx-dns-query/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns php jdwx_dns_query
python3 parsarium.py run dns php jdwx_dns_query controls/dns/response.bin
python3 parsarium.py replay dns php jdwx_dns_query CORPUS_DIR runs/dns-jdwx_dns_query-replay
python3 parsarium.py afl build dns php jdwx_dns_query
python3 parsarium.py afl prepare dns php jdwx_dns_query runs/dns-jdwx_dns_query-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
