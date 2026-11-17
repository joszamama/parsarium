# pear/net_dns2 — DNS / PHP

Pinned release: `v2.0.7`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/php/pear-net-dns2/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns php pear_net_dns2
python3 parsarium.py run dns php pear_net_dns2 controls/dns/response.bin
python3 parsarium.py replay dns php pear_net_dns2 CORPUS_DIR runs/dns-pear_net_dns2-replay
python3 parsarium.py afl build dns php pear_net_dns2
python3 parsarium.py afl prepare dns php pear_net_dns2 runs/dns-pear_net_dns2-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
