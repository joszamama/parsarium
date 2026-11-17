# hns-dns-wire — DNS / Rust

Pinned release: `0.2.2`. [Manifest](manifest.json) · [verification receipt](verification.json)

[API, control result, and parser family](../../../../catalog/dns/rust/hns-dns-wire/README.md)

## Run from the repository root

```sh
python3 parsarium.py build dns rust hns_dns_wire
python3 parsarium.py run dns rust hns_dns_wire controls/dns/response.bin
python3 parsarium.py replay dns rust hns_dns_wire CORPUS_DIR runs/dns-hns_dns_wire-replay
python3 parsarium.py afl build dns rust hns_dns_wire
python3 parsarium.py afl prepare dns rust hns_dns_wire runs/dns-hns_dns_wire-afl
```

Replace `CORPUS_DIR` with a directory of matching files. The AFL++ command prepares a seeded run; it does not start a campaign.
